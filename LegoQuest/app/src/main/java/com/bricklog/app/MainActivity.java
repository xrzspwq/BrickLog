package com.bricklog.app;

import android.app.Activity;
import android.os.Bundle;
import android.os.Build;
import android.graphics.Insets;
import android.view.WindowInsets;
import android.widget.FrameLayout;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.webkit.ValueCallback;
import android.webkit.JavascriptInterface;
import android.content.Intent;
import android.net.Uri;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import java.io.IOException;

public class MainActivity extends Activity {
    private WebView web;
    private ValueCallback<Uri[]> fileCallback;
    private String pendingBackup;
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(0xff100e17);
        getWindow().setNavigationBarColor(0xff100e17);
        getWindow().getDecorView().setSystemUiVisibility(0);
        web = new WebView(this);
        web.getSettings().setJavaScriptEnabled(true);
        web.getSettings().setDomStorageEnabled(true);
        web.addJavascriptInterface(new Object() {
            @JavascriptInterface public void exportBackup(String json) {
                pendingBackup = json;
                Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType("application/json").putExtra(Intent.EXTRA_TITLE, "bricklog-backup.json");
                startActivityForResult(intent, 42);
            }
        }, "BrickLogNative");
        web.setWebChromeClient(new WebChromeClient() {
            @Override public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if (fileCallback != null) fileCallback.onReceiveValue(null);
                fileCallback = callback;
                try { startActivityForResult(params.createIntent(), 43); return true; }
                catch (Exception e) { fileCallback = null; return false; }
            }
        });
        web.setWebViewClient(new WebViewClient() {
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                if ("app.bricklog.local".equals(request.getUrl().getHost())) {
                    String path = request.getUrl().getPath();
                    String asset = "index.html";
                    String mime = "text/html";
                    if (path != null && path.matches("/covers/[a-f0-9]{20}\\.jpg")) {
                        asset = path.substring(1);
                        mime = "image/jpeg";
                    } else if (path != null && !path.equals("/") && !path.equals("/index.html")) {
                        return new WebResourceResponse("text/plain", "UTF-8", 404, "Not Found", java.util.Collections.emptyMap(), new java.io.ByteArrayInputStream(new byte[0]));
                    }
                    try { return new WebResourceResponse(mime, "UTF-8", getAssets().open(asset)); }
                    catch (IOException e) { return null; }
                }
                return null;
            }
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                if (!"app.bricklog.local".equals(request.getUrl().getHost())) {
                    try { startActivity(new android.content.Intent(android.content.Intent.ACTION_VIEW, request.getUrl())); } catch (Exception ignored) {}
                    return true;
                }
                return false;
            }
        });
        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(0xff100e17);
        root.addView(web, new FrameLayout.LayoutParams(
            FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT));
        // Android 15 enforces edge-to-edge for apps targeting SDK 35. Earlier
        // versions already fit the content below the bars by default; do not
        // add padding there or the insets would be applied twice.
        if (Build.VERSION.SDK_INT >= 35) {
            root.setOnApplyWindowInsetsListener((view, insets) -> {
                int types = WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout();
                Insets safe = insets.getInsets(types);
                view.setPadding(safe.left, safe.top, safe.right, safe.bottom);
                // Keep IME insets available to the WebView for the keyboard.
                return new WindowInsets.Builder(insets).setInsets(types, Insets.NONE).build();
            });
        }
        setContentView(root);
        if (Build.VERSION.SDK_INT >= 35) root.requestApplyInsets();
        web.loadUrl("https://app.bricklog.local/index.html");
    }
    @Override protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request, result, data);
        if (request == 43 && fileCallback != null) {
            fileCallback.onReceiveValue(WebChromeClient.FileChooserParams.parseResult(result, data));
            fileCallback = null;
        } else if (request == 42 && result == RESULT_OK && data != null && pendingBackup != null) {
            try (java.io.OutputStream out = getContentResolver().openOutputStream(data.getData())) {
                if (out != null) out.write(pendingBackup.getBytes(java.nio.charset.StandardCharsets.UTF_8));
            } catch (Exception e) { android.widget.Toast.makeText(this, "Could not save backup", android.widget.Toast.LENGTH_LONG).show(); }
            pendingBackup = null;
        }
    }
    @Override public void onBackPressed() { web.evaluateJavascript("window.handleBack && window.handleBack()", null); }
}

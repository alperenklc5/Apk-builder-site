.class public Lcom/alperenkilic/webwrapperbase/MainActivity;
.super Landroidx/appcompat/app/AppCompatActivity;
.source "MainActivity.java"


# instance fields
.field private targetUrl:Ljava/lang/String;

.field private webView:Landroid/webkit/WebView;


# direct methods
.method static bridge synthetic -$$Nest$fgetwebView(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/webkit/WebView;
    .locals 0

    iget-object p0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->webView:Landroid/webkit/WebView;

    return-object p0
.end method

.method public constructor <init>()V
    .locals 1

    .line 13
    invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V

    .line 16
    const-string v0, "https://www.google.com"

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->targetUrl:Ljava/lang/String;

    return-void
.end method

.method private readConfigFromAssets()V
    .locals 7

    .line 66
    const-string v0, "site_url"

    :try_start_0
    invoke-virtual {p0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getAssets()Landroid/content/res/AssetManager;

    move-result-object v1

    const-string v2, "app_config.json"

    invoke-virtual {v1, v2}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;

    move-result-object v1

    .line 67
    .local v1, "is":Ljava/io/InputStream;
    invoke-virtual {v1}, Ljava/io/InputStream;->available()I

    move-result v2

    .line 68
    .local v2, "size":I
    new-array v3, v2, [B

    .line 69
    .local v3, "buffer":[B
    invoke-virtual {v1, v3}, Ljava/io/InputStream;->read([B)I

    .line 70
    invoke-virtual {v1}, Ljava/io/InputStream;->close()V

    .line 72
    new-instance v4, Ljava/lang/String;

    sget-object v5, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-direct {v4, v3, v5}, Ljava/lang/String;-><init>([BLjava/nio/charset/Charset;)V

    .line 73
    .local v4, "jsonString":Ljava/lang/String;
    new-instance v5, Lorg/json/JSONObject;

    invoke-direct {v5, v4}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    .line 75
    .local v5, "jsonObject":Lorg/json/JSONObject;
    invoke-virtual {v5, v0}, Lorg/json/JSONObject;->has(Ljava/lang/String;)Z

    move-result v6

    if-eqz v6, :cond_0

    .line 76
    invoke-virtual {v5, v0}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->targetUrl:Ljava/lang/String;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 81
    .end local v1    # "is":Ljava/io/InputStream;
    .end local v2    # "size":I
    .end local v3    # "buffer":[B
    .end local v4    # "jsonString":Ljava/lang/String;
    .end local v5    # "jsonObject":Lorg/json/JSONObject;
    :cond_0
    goto :goto_0

    .line 79
    :catch_0
    move-exception v0

    .line 80
    .local v0, "e":Ljava/lang/Exception;
    invoke-virtual {v0}, Ljava/lang/Exception;->printStackTrace()V

    .line 82
    .end local v0    # "e":Ljava/lang/Exception;
    :goto_0
    return-void
.end method


# virtual methods
.method protected onCreate(Landroid/os/Bundle;)V
    .locals 4
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .line 20
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    .line 24
    :try_start_0
    invoke-virtual {p0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getSupportActionBar()Landroidx/appcompat/app/ActionBar;

    move-result-object v0

    if-eqz v0, :cond_0

    .line 25
    invoke-virtual {p0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getSupportActionBar()Landroidx/appcompat/app/ActionBar;

    move-result-object v0

    invoke-virtual {v0}, Landroidx/appcompat/app/ActionBar;->hide()V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 29
    :cond_0
    goto :goto_0

    .line 27
    :catch_0
    move-exception v0

    .line 28
    .local v0, "e":Ljava/lang/Exception;
    invoke-virtual {v0}, Ljava/lang/Exception;->printStackTrace()V

    .line 31
    .end local v0    # "e":Ljava/lang/Exception;
    :goto_0
    sget v0, Lcom/alperenkilic/webwrapperbase/R$layout;->activity_main:I

    invoke-virtual {p0, v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->setContentView(I)V

    .line 33
    sget v0, Lcom/alperenkilic/webwrapperbase/R$id;->myWebView:I

    invoke-virtual {p0, v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/webkit/WebView;

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->webView:Landroid/webkit/WebView;

    .line 36
    invoke-direct {p0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->readConfigFromAssets()V

    .line 39
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->webView:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;

    move-result-object v0

    .line 40
    .local v0, "webSettings":Landroid/webkit/WebSettings;
    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V

    .line 41
    invoke-virtual {v0, v1}, Landroid/webkit/WebSettings;->setDomStorageEnabled(Z)V

    .line 43
    iget-object v2, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->webView:Landroid/webkit/WebView;

    new-instance v3, Landroid/webkit/WebViewClient;

    invoke-direct {v3}, Landroid/webkit/WebViewClient;-><init>()V

    invoke-virtual {v2, v3}, Landroid/webkit/WebView;->setWebViewClient(Landroid/webkit/WebViewClient;)V

    .line 46
    iget-object v2, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->webView:Landroid/webkit/WebView;

    iget-object v3, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->targetUrl:Ljava/lang/String;

    invoke-virtual {v2, v3}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V

    .line 50
    invoke-virtual {p0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getOnBackPressedDispatcher()Landroidx/activity/OnBackPressedDispatcher;

    move-result-object v2

    new-instance v3, Lcom/alperenkilic/webwrapperbase/MainActivity$1;

    invoke-direct {v3, p0, v1}, Lcom/alperenkilic/webwrapperbase/MainActivity$1;-><init>(Lcom/alperenkilic/webwrapperbase/MainActivity;Z)V

    invoke-virtual {v2, p0, v3}, Landroidx/activity/OnBackPressedDispatcher;->addCallback(Landroidx/lifecycle/LifecycleOwner;Landroidx/activity/OnBackPressedCallback;)V

    .line 61
    return-void
.end method

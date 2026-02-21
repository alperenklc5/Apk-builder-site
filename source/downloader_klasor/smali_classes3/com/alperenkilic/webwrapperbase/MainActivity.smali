.class public Lcom/alperenkilic/webwrapperbase/MainActivity;
.super Landroidx/appcompat/app/AppCompatActivity;
.source "MainActivity.java"


# instance fields
.field private btnClosePanel:Landroid/widget/Button;

.field private btnOpenPanel:Lcom/google/android/material/floatingactionbutton/FloatingActionButton;

.field private btnStartDownload:Landroid/widget/Button;

.field private final httpClient:Lokhttp3/OkHttpClient;

.field private inputLink:Landroid/widget/EditText;

.field private linkPanel:Landroid/widget/LinearLayout;

.field private loadingLayout:Landroid/widget/LinearLayout;

.field private targetUrl:Ljava/lang/String;

.field private webView:Landroid/webkit/WebView;


# direct methods
.method static bridge synthetic -$$Nest$fgetbtnOpenPanel(Lcom/alperenkilic/webwrapperbase/MainActivity;)Lcom/google/android/material/floatingactionbutton/FloatingActionButton;
    .locals 0

    iget-object p0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->btnOpenPanel:Lcom/google/android/material/floatingactionbutton/FloatingActionButton;

    return-object p0
.end method

.method static bridge synthetic -$$Nest$fgetlinkPanel(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/widget/LinearLayout;
    .locals 0

    iget-object p0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->linkPanel:Landroid/widget/LinearLayout;

    return-object p0
.end method

.method static bridge synthetic -$$Nest$fgetloadingLayout(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/widget/LinearLayout;
    .locals 0

    iget-object p0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->loadingLayout:Landroid/widget/LinearLayout;

    return-object p0
.end method

.method static bridge synthetic -$$Nest$fgetwebView(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/webkit/WebView;
    .locals 0

    iget-object p0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->webView:Landroid/webkit/WebView;

    return-object p0
.end method

.method static bridge synthetic -$$Nest$mcloseLoadingScreen(Lcom/alperenkilic/webwrapperbase/MainActivity;Ljava/lang/String;)V
    .locals 0

    invoke-direct {p0, p1}, Lcom/alperenkilic/webwrapperbase/MainActivity;->closeLoadingScreen(Ljava/lang/String;)V

    return-void
.end method

.method static bridge synthetic -$$Nest$mstartDownload(Lcom/alperenkilic/webwrapperbase/MainActivity;Ljava/lang/String;Ljava/lang/String;)V
    .locals 0

    invoke-direct {p0, p1, p2}, Lcom/alperenkilic/webwrapperbase/MainActivity;->startDownload(Ljava/lang/String;Ljava/lang/String;)V

    return-void
.end method

.method public constructor <init>()V
    .locals 4

    .line 40
    invoke-direct {p0}, Landroidx/appcompat/app/AppCompatActivity;-><init>()V

    .line 49
    const-string v0, "https://www.google.com"

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->targetUrl:Ljava/lang/String;

    .line 52
    new-instance v0, Lokhttp3/OkHttpClient$Builder;

    invoke-direct {v0}, Lokhttp3/OkHttpClient$Builder;-><init>()V

    sget-object v1, Ljava/util/concurrent/TimeUnit;->SECONDS:Ljava/util/concurrent/TimeUnit;

    .line 53
    const-wide/16 v2, 0x3c

    invoke-virtual {v0, v2, v3, v1}, Lokhttp3/OkHttpClient$Builder;->connectTimeout(JLjava/util/concurrent/TimeUnit;)Lokhttp3/OkHttpClient$Builder;

    move-result-object v0

    sget-object v1, Ljava/util/concurrent/TimeUnit;->SECONDS:Ljava/util/concurrent/TimeUnit;

    .line 54
    invoke-virtual {v0, v2, v3, v1}, Lokhttp3/OkHttpClient$Builder;->writeTimeout(JLjava/util/concurrent/TimeUnit;)Lokhttp3/OkHttpClient$Builder;

    move-result-object v0

    sget-object v1, Ljava/util/concurrent/TimeUnit;->SECONDS:Ljava/util/concurrent/TimeUnit;

    .line 55
    invoke-virtual {v0, v2, v3, v1}, Lokhttp3/OkHttpClient$Builder;->readTimeout(JLjava/util/concurrent/TimeUnit;)Lokhttp3/OkHttpClient$Builder;

    move-result-object v0

    .line 56
    invoke-virtual {v0}, Lokhttp3/OkHttpClient$Builder;->build()Lokhttp3/OkHttpClient;

    move-result-object v0

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->httpClient:Lokhttp3/OkHttpClient;

    .line 52
    return-void
.end method

.method private closeLoadingScreen(Ljava/lang/String;)V
    .locals 2
    .param p1, "message"    # Ljava/lang/String;

    .line 192
    new-instance v0, Landroid/os/Handler;

    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;

    move-result-object v1

    invoke-direct {v0, v1}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    new-instance v1, Lcom/alperenkilic/webwrapperbase/MainActivity$$ExternalSyntheticLambda3;

    invoke-direct {v1, p0, p1}, Lcom/alperenkilic/webwrapperbase/MainActivity$$ExternalSyntheticLambda3;-><init>(Lcom/alperenkilic/webwrapperbase/MainActivity;Ljava/lang/String;)V

    invoke-virtual {v0, v1}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z

    .line 197
    return-void
.end method

.method private getDirectLinkFromServer(Ljava/lang/String;)V
    .locals 6
    .param p1, "pageUrl"    # Ljava/lang/String;

    .line 144
    const-string v0, "http://hk0ww8o0kwko0s84884gckg0.164.68.113.20.sslip.io/get-video"

    .line 146
    .local v0, "apiUrl":Ljava/lang/String;
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "{\"url\":\""

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, "\"}"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    .line 148
    .local v1, "jsonBody":Ljava/lang/String;
    const-string v2, "application/json; charset=utf-8"

    invoke-static {v2}, Lokhttp3/MediaType;->get(Ljava/lang/String;)Lokhttp3/MediaType;

    move-result-object v2

    invoke-static {v1, v2}, Lokhttp3/RequestBody;->create(Ljava/lang/String;Lokhttp3/MediaType;)Lokhttp3/RequestBody;

    move-result-object v2

    .line 149
    .local v2, "body":Lokhttp3/RequestBody;
    new-instance v3, Lokhttp3/Request$Builder;

    invoke-direct {v3}, Lokhttp3/Request$Builder;-><init>()V

    .line 150
    invoke-virtual {v3, v0}, Lokhttp3/Request$Builder;->url(Ljava/lang/String;)Lokhttp3/Request$Builder;

    move-result-object v3

    .line 151
    invoke-virtual {v3, v2}, Lokhttp3/Request$Builder;->post(Lokhttp3/RequestBody;)Lokhttp3/Request$Builder;

    move-result-object v3

    .line 152
    invoke-virtual {v3}, Lokhttp3/Request$Builder;->build()Lokhttp3/Request;

    move-result-object v3

    .line 154
    .local v3, "request":Lokhttp3/Request;
    iget-object v4, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->httpClient:Lokhttp3/OkHttpClient;

    invoke-virtual {v4, v3}, Lokhttp3/OkHttpClient;->newCall(Lokhttp3/Request;)Lokhttp3/Call;

    move-result-object v4

    new-instance v5, Lcom/alperenkilic/webwrapperbase/MainActivity$2;

    invoke-direct {v5, p0}, Lcom/alperenkilic/webwrapperbase/MainActivity$2;-><init>(Lcom/alperenkilic/webwrapperbase/MainActivity;)V

    invoke-interface {v4, v5}, Lokhttp3/Call;->enqueue(Lokhttp3/Callback;)V

    .line 189
    return-void
.end method

.method private readConfigFromAssets()V
    .locals 7

    .line 231
    const-string v0, "site_url"

    :try_start_0
    invoke-virtual {p0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getAssets()Landroid/content/res/AssetManager;

    move-result-object v1

    const-string v2, "app_config.json"

    invoke-virtual {v1, v2}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;

    move-result-object v1

    .line 232
    .local v1, "is":Ljava/io/InputStream;
    invoke-virtual {v1}, Ljava/io/InputStream;->available()I

    move-result v2

    .line 233
    .local v2, "size":I
    new-array v3, v2, [B

    .line 234
    .local v3, "buffer":[B
    invoke-virtual {v1, v3}, Ljava/io/InputStream;->read([B)I

    .line 235
    invoke-virtual {v1}, Ljava/io/InputStream;->close()V

    .line 236
    new-instance v4, Ljava/lang/String;

    sget-object v5, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;

    invoke-direct {v4, v3, v5}, Ljava/lang/String;-><init>([BLjava/nio/charset/Charset;)V

    .line 237
    .local v4, "jsonString":Ljava/lang/String;
    new-instance v5, Lorg/json/JSONObject;

    invoke-direct {v5, v4}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    .line 238
    .local v5, "jsonObject":Lorg/json/JSONObject;
    invoke-virtual {v5, v0}, Lorg/json/JSONObject;->has(Ljava/lang/String;)Z

    move-result v6

    if-eqz v6, :cond_0

    invoke-virtual {v5, v0}, Lorg/json/JSONObject;->getString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->targetUrl:Ljava/lang/String;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 239
    .end local v1    # "is":Ljava/io/InputStream;
    .end local v2    # "size":I
    .end local v3    # "buffer":[B
    .end local v4    # "jsonString":Ljava/lang/String;
    .end local v5    # "jsonObject":Lorg/json/JSONObject;
    :cond_0
    goto :goto_0

    :catch_0
    move-exception v0

    .local v0, "e":Ljava/lang/Exception;
    invoke-virtual {v0}, Ljava/lang/Exception;->printStackTrace()V

    .line 240
    .end local v0    # "e":Ljava/lang/Exception;
    :goto_0
    return-void
.end method

.method private startDownload(Ljava/lang/String;Ljava/lang/String;)V
    .locals 7
    .param p1, "url"    # Ljava/lang/String;
    .param p2, "title"    # Ljava/lang/String;

    .line 200
    const-string v0, "_"

    sget v1, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v2, 0x1d

    const/4 v3, 0x0

    const/4 v4, 0x1

    if-ge v1, v2, :cond_0

    .line 201
    const-string v1, "android.permission.WRITE_EXTERNAL_STORAGE"

    invoke-static {p0, v1}, Landroidx/core/content/ContextCompat;->checkSelfPermission(Landroid/content/Context;Ljava/lang/String;)I

    move-result v2

    if-eqz v2, :cond_0

    .line 202
    new-array v0, v4, [Ljava/lang/String;

    aput-object v1, v0, v3

    invoke-static {p0, v0, v4}, Landroidx/core/app/ActivityCompat;->requestPermissions(Landroid/app/Activity;[Ljava/lang/String;I)V

    .line 203
    return-void

    .line 208
    :cond_0
    :try_start_0
    new-instance v1, Landroid/app/DownloadManager$Request;

    invoke-static {p1}, Landroid/net/Uri;->parse(Ljava/lang/String;)Landroid/net/Uri;

    move-result-object v2

    invoke-direct {v1, v2}, Landroid/app/DownloadManager$Request;-><init>(Landroid/net/Uri;)V

    .line 210
    .local v1, "request":Landroid/app/DownloadManager$Request;
    const-string v2, "[^a-zA-Z0-9.-]"

    invoke-virtual {p2, v2, v0}, Ljava/lang/String;->replaceAll(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 211
    .local v2, "safeTitle":Ljava/lang/String;
    invoke-virtual {v2}, Ljava/lang/String;->length()I

    move-result v5

    const/16 v6, 0x32

    if-le v5, v6, :cond_1

    invoke-virtual {v2, v3, v6}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v3

    move-object v2, v3

    .line 212
    :cond_1
    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    invoke-virtual {v0, v5, v6}, Ljava/lang/StringBuilder;->append(J)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v3, ".mp4"

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    .line 214
    .local v0, "fileName":Ljava/lang/String;
    invoke-virtual {v1, v0}, Landroid/app/DownloadManager$Request;->setTitle(Ljava/lang/CharSequence;)Landroid/app/DownloadManager$Request;

    .line 215
    const-string v3, "Video is Downloading"

    invoke-virtual {v1, v3}, Landroid/app/DownloadManager$Request;->setDescription(Ljava/lang/CharSequence;)Landroid/app/DownloadManager$Request;

    .line 216
    invoke-virtual {v1, v4}, Landroid/app/DownloadManager$Request;->setNotificationVisibility(I)Landroid/app/DownloadManager$Request;

    .line 217
    sget-object v3, Landroid/os/Environment;->DIRECTORY_DOWNLOADS:Ljava/lang/String;

    invoke-virtual {v1, v3, v0}, Landroid/app/DownloadManager$Request;->setDestinationInExternalPublicDir(Ljava/lang/String;Ljava/lang/String;)Landroid/app/DownloadManager$Request;

    .line 219
    const-string v3, "download"

    invoke-virtual {p0, v3}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getSystemService(Ljava/lang/String;)Ljava/lang/Object;

    move-result-object v3

    check-cast v3, Landroid/app/DownloadManager;

    .line 220
    .local v3, "dm":Landroid/app/DownloadManager;
    invoke-virtual {v3, v1}, Landroid/app/DownloadManager;->enqueue(Landroid/app/DownloadManager$Request;)J

    .line 222
    invoke-virtual {p0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getApplicationContext()Landroid/content/Context;

    move-result-object v5

    const-string v6, "Download Started!"

    invoke-static {v5, v6, v4}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v5

    invoke-virtual {v5}, Landroid/widget/Toast;->show()V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 226
    .end local v0    # "fileName":Ljava/lang/String;
    .end local v1    # "request":Landroid/app/DownloadManager$Request;
    .end local v2    # "safeTitle":Ljava/lang/String;
    .end local v3    # "dm":Landroid/app/DownloadManager;
    goto :goto_0

    .line 224
    :catch_0
    move-exception v0

    .line 225
    .local v0, "e":Ljava/lang/Exception;
    invoke-virtual {p0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getApplicationContext()Landroid/content/Context;

    move-result-object v1

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "Server Download Error: "

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v0}, Ljava/lang/Exception;->getMessage()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v1, v2, v4}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v1

    invoke-virtual {v1}, Landroid/widget/Toast;->show()V

    .line 227
    .end local v0    # "e":Ljava/lang/Exception;
    :goto_0
    return-void
.end method


# virtual methods
.method synthetic lambda$closeLoadingScreen$3$com-alperenkilic-webwrapperbase-MainActivity(Ljava/lang/String;)V
    .locals 2
    .param p1, "message"    # Ljava/lang/String;

    .line 193
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->loadingLayout:Landroid/widget/LinearLayout;

    const/16 v1, 0x8

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 194
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->btnOpenPanel:Lcom/google/android/material/floatingactionbutton/FloatingActionButton;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setVisibility(I)V

    .line 195
    const/4 v0, 0x1

    invoke-static {p0, p1, v0}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v0

    invoke-virtual {v0}, Landroid/widget/Toast;->show()V

    .line 196
    return-void
.end method

.method synthetic lambda$onCreate$0$com-alperenkilic-webwrapperbase-MainActivity(Landroid/view/View;)V
    .locals 3
    .param p1, "v"    # Landroid/view/View;

    .line 92
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->webView:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->getUrl()Ljava/lang/String;

    move-result-object v0

    .line 93
    .local v0, "currentUrl":Ljava/lang/String;
    iget-object v1, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->inputLink:Landroid/widget/EditText;

    invoke-virtual {v1, v0}, Landroid/widget/EditText;->setText(Ljava/lang/CharSequence;)V

    .line 94
    iget-object v1, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->linkPanel:Landroid/widget/LinearLayout;

    const/4 v2, 0x0

    invoke-virtual {v1, v2}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 95
    iget-object v1, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->btnOpenPanel:Lcom/google/android/material/floatingactionbutton/FloatingActionButton;

    const/16 v2, 0x8

    invoke-virtual {v1, v2}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setVisibility(I)V

    .line 96
    return-void
.end method

.method synthetic lambda$onCreate$1$com-alperenkilic-webwrapperbase-MainActivity(Landroid/view/View;)V
    .locals 2
    .param p1, "v"    # Landroid/view/View;

    .line 100
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->linkPanel:Landroid/widget/LinearLayout;

    const/16 v1, 0x8

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 101
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->btnOpenPanel:Lcom/google/android/material/floatingactionbutton/FloatingActionButton;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setVisibility(I)V

    .line 102
    return-void
.end method

.method synthetic lambda$onCreate$2$com-alperenkilic-webwrapperbase-MainActivity(Landroid/view/View;)V
    .locals 4
    .param p1, "v"    # Landroid/view/View;

    .line 106
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->inputLink:Landroid/widget/EditText;

    invoke-virtual {v0}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v0

    .line 107
    .local v0, "manualUrl":Ljava/lang/String;
    invoke-virtual {v0}, Ljava/lang/String;->isEmpty()Z

    move-result v1

    const/4 v2, 0x0

    if-nez v1, :cond_0

    .line 109
    iget-object v1, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->linkPanel:Landroid/widget/LinearLayout;

    const/16 v3, 0x8

    invoke-virtual {v1, v3}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 110
    iget-object v1, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->loadingLayout:Landroid/widget/LinearLayout;

    invoke-virtual {v1, v2}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 113
    invoke-direct {p0, v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getDirectLinkFromServer(Ljava/lang/String;)V

    goto :goto_0

    .line 115
    :cond_0
    const-string v1, "Please Enter a link!"

    invoke-static {p0, v1, v2}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v1

    invoke-virtual {v1}, Landroid/widget/Toast;->show()V

    .line 117
    :goto_0
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .locals 4
    .param p1, "savedInstanceState"    # Landroid/os/Bundle;

    .line 60
    invoke-super {p0, p1}, Landroidx/appcompat/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    .line 61
    :try_start_0
    invoke-virtual {p0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getSupportActionBar()Landroidx/appcompat/app/ActionBar;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-virtual {p0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getSupportActionBar()Landroidx/appcompat/app/ActionBar;

    move-result-object v0

    invoke-virtual {v0}, Landroidx/appcompat/app/ActionBar;->hide()V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    :catch_0
    move-exception v0

    .line 62
    :cond_0
    :goto_0
    sget v0, Lcom/alperenkilic/webwrapperbase/R$layout;->activity_main:I

    invoke-virtual {p0, v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->setContentView(I)V

    .line 65
    sget v0, Lcom/alperenkilic/webwrapperbase/R$id;->myWebView:I

    invoke-virtual {p0, v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/webkit/WebView;

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->webView:Landroid/webkit/WebView;

    .line 66
    sget v0, Lcom/alperenkilic/webwrapperbase/R$id;->btnOpenPanel:I

    invoke-virtual {p0, v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->btnOpenPanel:Lcom/google/android/material/floatingactionbutton/FloatingActionButton;

    .line 67
    sget v0, Lcom/alperenkilic/webwrapperbase/R$id;->loadingLayout:I

    invoke-virtual {p0, v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/LinearLayout;

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->loadingLayout:Landroid/widget/LinearLayout;

    .line 68
    sget v0, Lcom/alperenkilic/webwrapperbase/R$id;->linkPanel:I

    invoke-virtual {p0, v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/LinearLayout;

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->linkPanel:Landroid/widget/LinearLayout;

    .line 69
    sget v0, Lcom/alperenkilic/webwrapperbase/R$id;->inputLink:I

    invoke-virtual {p0, v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/EditText;

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->inputLink:Landroid/widget/EditText;

    .line 70
    sget v0, Lcom/alperenkilic/webwrapperbase/R$id;->btnStartDownload:I

    invoke-virtual {p0, v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->btnStartDownload:Landroid/widget/Button;

    .line 71
    sget v0, Lcom/alperenkilic/webwrapperbase/R$id;->btnClosePanel:I

    invoke-virtual {p0, v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/Button;

    iput-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->btnClosePanel:Landroid/widget/Button;

    .line 73
    invoke-direct {p0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->readConfigFromAssets()V

    .line 76
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->webView:Landroid/webkit/WebView;

    invoke-virtual {v0}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;

    move-result-object v0

    .line 77
    .local v0, "webSettings":Landroid/webkit/WebSettings;
    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V

    .line 78
    invoke-virtual {v0, v1}, Landroid/webkit/WebSettings;->setDomStorageEnabled(Z)V

    .line 79
    invoke-virtual {v0, v1}, Landroid/webkit/WebSettings;->setAllowFileAccess(Z)V

    .line 80
    const-string v2, "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"

    invoke-virtual {v0, v2}, Landroid/webkit/WebSettings;->setUserAgentString(Ljava/lang/String;)V

    .line 82
    invoke-static {}, Landroid/webkit/CookieManager;->getInstance()Landroid/webkit/CookieManager;

    move-result-object v2

    invoke-virtual {v2, v1}, Landroid/webkit/CookieManager;->setAcceptCookie(Z)V

    .line 83
    nop

    .line 84
    invoke-static {}, Landroid/webkit/CookieManager;->getInstance()Landroid/webkit/CookieManager;

    move-result-object v2

    iget-object v3, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->webView:Landroid/webkit/WebView;

    invoke-virtual {v2, v3, v1}, Landroid/webkit/CookieManager;->setAcceptThirdPartyCookies(Landroid/webkit/WebView;Z)V

    .line 87
    iget-object v2, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->webView:Landroid/webkit/WebView;

    new-instance v3, Landroid/webkit/WebViewClient;

    invoke-direct {v3}, Landroid/webkit/WebViewClient;-><init>()V

    invoke-virtual {v2, v3}, Landroid/webkit/WebView;->setWebViewClient(Landroid/webkit/WebViewClient;)V

    .line 88
    iget-object v2, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->webView:Landroid/webkit/WebView;

    iget-object v3, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->targetUrl:Ljava/lang/String;

    invoke-virtual {v2, v3}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V

    .line 91
    iget-object v2, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->btnOpenPanel:Lcom/google/android/material/floatingactionbutton/FloatingActionButton;

    new-instance v3, Lcom/alperenkilic/webwrapperbase/MainActivity$$ExternalSyntheticLambda0;

    invoke-direct {v3, p0}, Lcom/alperenkilic/webwrapperbase/MainActivity$$ExternalSyntheticLambda0;-><init>(Lcom/alperenkilic/webwrapperbase/MainActivity;)V

    invoke-virtual {v2, v3}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 99
    iget-object v2, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->btnClosePanel:Landroid/widget/Button;

    new-instance v3, Lcom/alperenkilic/webwrapperbase/MainActivity$$ExternalSyntheticLambda1;

    invoke-direct {v3, p0}, Lcom/alperenkilic/webwrapperbase/MainActivity$$ExternalSyntheticLambda1;-><init>(Lcom/alperenkilic/webwrapperbase/MainActivity;)V

    invoke-virtual {v2, v3}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 105
    iget-object v2, p0, Lcom/alperenkilic/webwrapperbase/MainActivity;->btnStartDownload:Landroid/widget/Button;

    new-instance v3, Lcom/alperenkilic/webwrapperbase/MainActivity$$ExternalSyntheticLambda2;

    invoke-direct {v3, p0}, Lcom/alperenkilic/webwrapperbase/MainActivity$$ExternalSyntheticLambda2;-><init>(Lcom/alperenkilic/webwrapperbase/MainActivity;)V

    invoke-virtual {v2, v3}, Landroid/widget/Button;->setOnClickListener(Landroid/view/View$OnClickListener;)V

    .line 120
    invoke-virtual {p0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getOnBackPressedDispatcher()Landroidx/activity/OnBackPressedDispatcher;

    move-result-object v2

    new-instance v3, Lcom/alperenkilic/webwrapperbase/MainActivity$1;

    invoke-direct {v3, p0, v1}, Lcom/alperenkilic/webwrapperbase/MainActivity$1;-><init>(Lcom/alperenkilic/webwrapperbase/MainActivity;Z)V

    invoke-virtual {v2, p0, v3}, Landroidx/activity/OnBackPressedDispatcher;->addCallback(Landroidx/lifecycle/LifecycleOwner;Landroidx/activity/OnBackPressedCallback;)V

    .line 140
    return-void
.end method

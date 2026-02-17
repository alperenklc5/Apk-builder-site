.class Lcom/alperenkilic/webwrapperbase/MainActivity$2;
.super Ljava/lang/Object;
.source "MainActivity.java"

# interfaces
.implements Lokhttp3/Callback;


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/alperenkilic/webwrapperbase/MainActivity;->getDirectLinkFromServer(Ljava/lang/String;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;


# direct methods
.method constructor <init>(Lcom/alperenkilic/webwrapperbase/MainActivity;)V
    .locals 0
    .param p1, "this$0"    # Lcom/alperenkilic/webwrapperbase/MainActivity;
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010
        }
        names = {
            null
        }
    .end annotation

    .line 154
    iput-object p1, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$2;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method synthetic lambda$onResponse$0$com-alperenkilic-webwrapperbase-MainActivity$2(Ljava/lang/String;Ljava/lang/String;)V
    .locals 2
    .param p1, "directUrl"    # Ljava/lang/String;
    .param p2, "title"    # Ljava/lang/String;

    .line 173
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$2;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-static {v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$fgetloadingLayout(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/widget/LinearLayout;

    move-result-object v0

    const/16 v1, 0x8

    invoke-virtual {v0, v1}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 174
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$2;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-static {v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$fgetbtnOpenPanel(Lcom/alperenkilic/webwrapperbase/MainActivity;)Lcom/google/android/material/floatingactionbutton/FloatingActionButton;

    move-result-object v0

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setVisibility(I)V

    .line 175
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$2;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-static {v0, p1, p2}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$mstartDownload(Lcom/alperenkilic/webwrapperbase/MainActivity;Ljava/lang/String;Ljava/lang/String;)V

    .line 176
    return-void
.end method

.method public onFailure(Lokhttp3/Call;Ljava/io/IOException;)V
    .locals 3
    .param p1, "call"    # Lokhttp3/Call;
    .param p2, "e"    # Ljava/io/IOException;

    .line 157
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$2;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "Sunucu Hatas\u0131: "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {p2}, Ljava/io/IOException;->getMessage()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$mcloseLoadingScreen(Lcom/alperenkilic/webwrapperbase/MainActivity;Ljava/lang/String;)V

    .line 158
    return-void
.end method

.method public onResponse(Lokhttp3/Call;Lokhttp3/Response;)V
    .locals 7
    .param p1, "call"    # Lokhttp3/Call;
    .param p2, "response"    # Lokhttp3/Response;
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .line 162
    invoke-virtual {p2}, Lokhttp3/Response;->isSuccessful()Z

    move-result v0

    if-eqz v0, :cond_1

    .line 163
    invoke-virtual {p2}, Lokhttp3/Response;->body()Lokhttp3/ResponseBody;

    move-result-object v0

    invoke-virtual {v0}, Lokhttp3/ResponseBody;->string()Ljava/lang/String;

    move-result-object v0

    .line 165
    .local v0, "responseData":Ljava/lang/String;
    :try_start_0
    new-instance v1, Lorg/json/JSONObject;

    invoke-direct {v1, v0}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V

    .line 166
    .local v1, "json":Lorg/json/JSONObject;
    const-string v2, "status"

    invoke-virtual {v1, v2}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v2

    .line 168
    .local v2, "status":Ljava/lang/String;
    const-string v3, "success"

    invoke-virtual {v3, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-eqz v3, :cond_0

    .line 169
    const-string v3, "url"

    invoke-virtual {v1, v3}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    .line 170
    .local v3, "directUrl":Ljava/lang/String;
    const-string v4, "title"

    const-string v5, "video"

    invoke-virtual {v1, v4, v5}, Lorg/json/JSONObject;->optString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object v4

    .line 172
    .local v4, "title":Ljava/lang/String;
    new-instance v5, Landroid/os/Handler;

    invoke-static {}, Landroid/os/Looper;->getMainLooper()Landroid/os/Looper;

    move-result-object v6

    invoke-direct {v5, v6}, Landroid/os/Handler;-><init>(Landroid/os/Looper;)V

    new-instance v6, Lcom/alperenkilic/webwrapperbase/MainActivity$2$$ExternalSyntheticLambda0;

    invoke-direct {v6, p0, v3, v4}, Lcom/alperenkilic/webwrapperbase/MainActivity$2$$ExternalSyntheticLambda0;-><init>(Lcom/alperenkilic/webwrapperbase/MainActivity$2;Ljava/lang/String;Ljava/lang/String;)V

    invoke-virtual {v5, v6}, Landroid/os/Handler;->post(Ljava/lang/Runnable;)Z

    .line 177
    nop

    .end local v3    # "directUrl":Ljava/lang/String;
    .end local v4    # "title":Ljava/lang/String;
    goto :goto_0

    .line 178
    :cond_0
    const-string v3, "message"

    invoke-virtual {v1, v3}, Lorg/json/JSONObject;->optString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v3

    .line 179
    .local v3, "msg":Ljava/lang/String;
    iget-object v4, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$2;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, "Hata: "

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-static {v4, v5}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$mcloseLoadingScreen(Lcom/alperenkilic/webwrapperbase/MainActivity;Ljava/lang/String;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 183
    .end local v1    # "json":Lorg/json/JSONObject;
    .end local v2    # "status":Ljava/lang/String;
    .end local v3    # "msg":Ljava/lang/String;
    :goto_0
    goto :goto_1

    .line 181
    :catch_0
    move-exception v1

    .line 182
    .local v1, "e":Ljava/lang/Exception;
    iget-object v2, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$2;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    const-string v3, "Veri Hatas\u0131!"

    invoke-static {v2, v3}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$mcloseLoadingScreen(Lcom/alperenkilic/webwrapperbase/MainActivity;Ljava/lang/String;)V

    .line 184
    .end local v0    # "responseData":Ljava/lang/String;
    .end local v1    # "e":Ljava/lang/Exception;
    :goto_1
    goto :goto_2

    .line 185
    :cond_1
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$2;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "Sunucu Hatas\u0131 (Kod: "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {p2}, Lokhttp3/Response;->code()I

    move-result v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ")"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$mcloseLoadingScreen(Lcom/alperenkilic/webwrapperbase/MainActivity;Ljava/lang/String;)V

    .line 187
    :goto_2
    return-void
.end method

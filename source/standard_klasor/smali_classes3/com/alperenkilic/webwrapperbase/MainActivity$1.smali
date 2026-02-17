.class Lcom/alperenkilic/webwrapperbase/MainActivity$1;
.super Landroidx/activity/OnBackPressedCallback;
.source "MainActivity.java"


# annotations
.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/alperenkilic/webwrapperbase/MainActivity;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x0
    name = null
.end annotation


# instance fields
.field final synthetic this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;


# direct methods
.method constructor <init>(Lcom/alperenkilic/webwrapperbase/MainActivity;Z)V
    .locals 0
    .param p1, "this$0"    # Lcom/alperenkilic/webwrapperbase/MainActivity;
    .param p2, "arg0"    # Z
    .annotation system Ldalvik/annotation/MethodParameters;
        accessFlags = {
            0x8010,
            0x0
        }
        names = {
            null,
            null
        }
    .end annotation

    .line 50
    iput-object p1, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-direct {p0, p2}, Landroidx/activity/OnBackPressedCallback;-><init>(Z)V

    return-void
.end method


# virtual methods
.method public handleOnBackPressed()V
    .locals 1

    .line 53
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-static {v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$fgetwebView(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/webkit/WebView;

    move-result-object v0

    invoke-virtual {v0}, Landroid/webkit/WebView;->canGoBack()Z

    move-result v0

    if-eqz v0, :cond_0

    .line 54
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-static {v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$fgetwebView(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/webkit/WebView;

    move-result-object v0

    invoke-virtual {v0}, Landroid/webkit/WebView;->goBack()V

    goto :goto_0

    .line 56
    :cond_0
    const/4 v0, 0x0

    invoke-virtual {p0, v0}, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->setEnabled(Z)V

    .line 57
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-virtual {v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getOnBackPressedDispatcher()Landroidx/activity/OnBackPressedDispatcher;

    move-result-object v0

    invoke-virtual {v0}, Landroidx/activity/OnBackPressedDispatcher;->onBackPressed()V

    .line 59
    :goto_0
    return-void
.end method

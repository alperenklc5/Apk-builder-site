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

    .line 120
    iput-object p1, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-direct {p0, p2}, Landroidx/activity/OnBackPressedCallback;-><init>(Z)V

    return-void
.end method


# virtual methods
.method public handleOnBackPressed()V
    .locals 4

    .line 124
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-static {v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$fgetlinkPanel(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/widget/LinearLayout;

    move-result-object v0

    invoke-virtual {v0}, Landroid/widget/LinearLayout;->getVisibility()I

    move-result v0

    .line 130
    iget-object v1, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    .line 124
    const/16 v2, 0x8

    const/4 v3, 0x0

    if-nez v0, :cond_0

    .line 125
    invoke-static {v1}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$fgetlinkPanel(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/widget/LinearLayout;

    move-result-object v0

    invoke-virtual {v0, v2}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 126
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-static {v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$fgetbtnOpenPanel(Lcom/alperenkilic/webwrapperbase/MainActivity;)Lcom/google/android/material/floatingactionbutton/FloatingActionButton;

    move-result-object v0

    invoke-virtual {v0, v3}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setVisibility(I)V

    .line 127
    return-void

    .line 130
    :cond_0
    invoke-static {v1}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$fgetloadingLayout(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/widget/LinearLayout;

    move-result-object v0

    invoke-virtual {v0}, Landroid/widget/LinearLayout;->getVisibility()I

    move-result v0

    .line 136
    iget-object v1, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    .line 130
    if-nez v0, :cond_1

    .line 131
    invoke-static {v1}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$fgetloadingLayout(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/widget/LinearLayout;

    move-result-object v0

    invoke-virtual {v0, v2}, Landroid/widget/LinearLayout;->setVisibility(I)V

    .line 132
    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-static {v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$fgetbtnOpenPanel(Lcom/alperenkilic/webwrapperbase/MainActivity;)Lcom/google/android/material/floatingactionbutton/FloatingActionButton;

    move-result-object v0

    invoke-virtual {v0, v3}, Lcom/google/android/material/floatingactionbutton/FloatingActionButton;->setVisibility(I)V

    .line 133
    return-void

    .line 136
    :cond_1
    invoke-static {v1}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$fgetwebView(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/webkit/WebView;

    move-result-object v0

    invoke-virtual {v0}, Landroid/webkit/WebView;->canGoBack()Z

    move-result v0

    if-eqz v0, :cond_2

    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-static {v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->-$$Nest$fgetwebView(Lcom/alperenkilic/webwrapperbase/MainActivity;)Landroid/webkit/WebView;

    move-result-object v0

    invoke-virtual {v0}, Landroid/webkit/WebView;->goBack()V

    goto :goto_0

    .line 137
    :cond_2
    invoke-virtual {p0, v3}, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->setEnabled(Z)V

    iget-object v0, p0, Lcom/alperenkilic/webwrapperbase/MainActivity$1;->this$0:Lcom/alperenkilic/webwrapperbase/MainActivity;

    invoke-virtual {v0}, Lcom/alperenkilic/webwrapperbase/MainActivity;->getOnBackPressedDispatcher()Landroidx/activity/OnBackPressedDispatcher;

    move-result-object v0

    invoke-virtual {v0}, Landroidx/activity/OnBackPressedDispatcher;->onBackPressed()V

    .line 138
    :goto_0
    return-void
.end method

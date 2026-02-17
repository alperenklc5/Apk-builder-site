.class public final Lokhttp3/internal/ws/WebSocketExtensions$Companion;
.super Ljava/lang/Object;
.source "WebSocketExtensions.kt"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lokhttp3/internal/ws/WebSocketExtensions;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x19
    name = "Companion"
.end annotation

.annotation runtime Lkotlin/Metadata;
    bv = {
        0x1,
        0x0,
        0x3
    }
    d1 = {
        "\u0000\u001e\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\u0008\u0002\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\u0008\u0086\u0003\u0018\u00002\u00020\u0001B\u0007\u0008\u0002\u00a2\u0006\u0002\u0010\u0002J\u000e\u0010\u0005\u001a\u00020\u00062\u0006\u0010\u0007\u001a\u00020\u0008R\u000e\u0010\u0003\u001a\u00020\u0004X\u0082T\u00a2\u0006\u0002\n\u0000\u00a8\u0006\t"
    }
    d2 = {
        "Lokhttp3/internal/ws/WebSocketExtensions$Companion;",
        "",
        "()V",
        "HEADER_WEB_SOCKET_EXTENSION",
        "",
        "parse",
        "Lokhttp3/internal/ws/WebSocketExtensions;",
        "responseHeaders",
        "Lokhttp3/Headers;",
        "okhttp"
    }
    k = 0x1
    mv = {
        0x1,
        0x4,
        0x0
    }
.end annotation


# direct methods
.method private constructor <init>()V
    .locals 0

    .line 90
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public synthetic constructor <init>(Lkotlin/jvm/internal/DefaultConstructorMarker;)V
    .locals 0
    .param p1, "$constructor_marker"    # Lkotlin/jvm/internal/DefaultConstructorMarker;

    .line 90
    invoke-direct {p0}, Lokhttp3/internal/ws/WebSocketExtensions$Companion;-><init>()V

    return-void
.end method


# virtual methods
.method public final parse(Lokhttp3/Headers;)Lokhttp3/internal/ws/WebSocketExtensions;
    .locals 23
    .param p1, "responseHeaders"    # Lokhttp3/Headers;
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    move-object/from16 v0, p1

    const-string v1, "responseHeaders"

    invoke-static {v0, v1}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullParameter(Ljava/lang/Object;Ljava/lang/String;)V

    .line 98
    const/4 v1, 0x0

    .line 99
    .local v1, "compressionEnabled":Z
    const/4 v2, 0x0

    move-object v3, v2

    check-cast v3, Ljava/lang/Integer;

    .line 100
    .local v3, "clientMaxWindowBits":Ljava/lang/Integer;
    const/4 v4, 0x0

    .line 101
    .local v4, "clientNoContextTakeover":Z
    move-object v5, v2

    check-cast v5, Ljava/lang/Integer;

    .line 102
    .local v5, "serverMaxWindowBits":Ljava/lang/Integer;
    const/4 v6, 0x0

    .line 103
    .local v6, "serverNoContextTakeover":Z
    const/4 v7, 0x0

    .line 106
    .local v7, "unexpectedValues":Z
    invoke-virtual {v0}, Lokhttp3/Headers;->size()I

    move-result v8

    const/4 v9, 0x0

    move v11, v1

    move-object v12, v3

    move v13, v4

    move-object v14, v5

    move v15, v6

    move/from16 v16, v7

    .end local v1    # "compressionEnabled":Z
    .end local v3    # "clientMaxWindowBits":Ljava/lang/Integer;
    .end local v4    # "clientNoContextTakeover":Z
    .end local v5    # "serverMaxWindowBits":Ljava/lang/Integer;
    .end local v6    # "serverNoContextTakeover":Z
    .end local v7    # "unexpectedValues":Z
    .local v11, "compressionEnabled":Z
    .local v12, "clientMaxWindowBits":Ljava/lang/Integer;
    .local v13, "clientNoContextTakeover":Z
    .local v14, "serverMaxWindowBits":Ljava/lang/Integer;
    .local v15, "serverNoContextTakeover":Z
    .local v16, "unexpectedValues":Z
    :goto_0
    if-ge v9, v8, :cond_14

    .line 107
    .local v9, "i":I
    invoke-virtual {v0, v9}, Lokhttp3/Headers;->name(I)Ljava/lang/String;

    move-result-object v1

    const-string v3, "Sec-WebSocket-Extensions"

    const/4 v4, 0x1

    invoke-static {v1, v3, v4}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v1

    if-nez v1, :cond_0

    .line 108
    goto/16 :goto_8

    .line 110
    :cond_0
    invoke-virtual {v0, v9}, Lokhttp3/Headers;->value(I)Ljava/lang/String;

    move-result-object v17

    .line 113
    .local v17, "header":Ljava/lang/String;
    const/4 v1, 0x0

    .line 114
    .local v1, "pos":I
    :goto_1
    invoke-virtual/range {v17 .. v17}, Ljava/lang/String;->length()I

    move-result v3

    if-ge v1, v3, :cond_13

    .line 115
    const/16 v21, 0x4

    const/16 v22, 0x0

    const/16 v18, 0x2c

    const/16 v20, 0x0

    move/from16 v19, v1

    .end local v1    # "pos":I
    .local v19, "pos":I
    invoke-static/range {v17 .. v22}, Lokhttp3/internal/Util;->delimiterOffset$default(Ljava/lang/String;CIIILjava/lang/Object;)I

    move-result v1

    .line 116
    move-object/from16 v3, v17

    move/from16 v5, v19

    .end local v17    # "header":Ljava/lang/String;
    .end local v19    # "pos":I
    .local v1, "extensionEnd":I
    .local v3, "header":Ljava/lang/String;
    .local v5, "pos":I
    const/16 v6, 0x3b

    invoke-static {v3, v6, v5, v1}, Lokhttp3/internal/Util;->delimiterOffset(Ljava/lang/String;CII)I

    move-result v7

    .line 117
    .local v7, "extensionTokenEnd":I
    invoke-static {v3, v5, v7}, Lokhttp3/internal/Util;->trimSubstring(Ljava/lang/String;II)Ljava/lang/String;

    move-result-object v10

    .line 118
    .local v10, "extensionToken":Ljava/lang/String;
    add-int/lit8 v5, v7, 0x1

    .line 120
    nop

    .line 121
    const-string v2, "permessage-deflate"

    invoke-static {v10, v2, v4}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v2

    if-eqz v2, :cond_12

    .line 122
    if-eqz v11, :cond_1

    const/16 v16, 0x1

    .line 123
    :cond_1
    const/4 v2, 0x1

    .line 126
    .end local v11    # "compressionEnabled":Z
    .local v2, "compressionEnabled":Z
    :goto_2
    if-ge v5, v1, :cond_11

    .line 127
    invoke-static {v3, v6, v5, v1}, Lokhttp3/internal/Util;->delimiterOffset(Ljava/lang/String;CII)I

    move-result v11

    .line 128
    .local v11, "parameterEnd":I
    const/16 v6, 0x3d

    invoke-static {v3, v6, v5, v11}, Lokhttp3/internal/Util;->delimiterOffset(Ljava/lang/String;CII)I

    move-result v6

    .line 129
    .local v6, "equals":I
    invoke-static {v3, v5, v6}, Lokhttp3/internal/Util;->trimSubstring(Ljava/lang/String;II)Ljava/lang/String;

    move-result-object v4

    .line 130
    .local v4, "name":Ljava/lang/String;
    if-ge v6, v11, :cond_2

    .line 131
    add-int/lit8 v0, v6, 0x1

    invoke-static {v3, v0, v11}, Lokhttp3/internal/Util;->trimSubstring(Ljava/lang/String;II)Ljava/lang/String;

    move-result-object v0

    const-string v20, "\""

    move/from16 v21, v1

    .end local v1    # "extensionEnd":I
    .local v21, "extensionEnd":I
    move-object/from16 v1, v20

    check-cast v1, Ljava/lang/CharSequence;

    invoke-static {v0, v1}, Lkotlin/text/StringsKt;->removeSurrounding(Ljava/lang/String;Ljava/lang/CharSequence;)Ljava/lang/String;

    move-result-object v0

    goto :goto_3

    .line 133
    .end local v21    # "extensionEnd":I
    .restart local v1    # "extensionEnd":I
    :cond_2
    move/from16 v21, v1

    .end local v1    # "extensionEnd":I
    .restart local v21    # "extensionEnd":I
    const/4 v0, 0x0

    .line 130
    :goto_3
    nop

    .line 135
    .local v0, "value":Ljava/lang/String;
    add-int/lit8 v5, v11, 0x1

    .line 136
    nop

    .line 137
    const-string v1, "client_max_window_bits"

    move-object/from16 v20, v0

    const/4 v0, 0x1

    .end local v0    # "value":Ljava/lang/String;
    .local v20, "value":Ljava/lang/String;
    invoke-static {v4, v1, v0}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v1

    if-eqz v1, :cond_6

    .line 138
    if-eqz v12, :cond_3

    const/16 v16, 0x1

    .line 139
    :cond_3
    if-eqz v20, :cond_4

    invoke-static/range {v20 .. v20}, Lkotlin/text/StringsKt;->toIntOrNull(Ljava/lang/String;)Ljava/lang/Integer;

    move-result-object v0

    goto :goto_4

    :cond_4
    const/4 v0, 0x0

    .line 140
    .end local v12    # "clientMaxWindowBits":Ljava/lang/Integer;
    .local v0, "clientMaxWindowBits":Ljava/lang/Integer;
    :goto_4
    if-nez v0, :cond_5

    const/4 v1, 0x1

    move-object v12, v0

    move/from16 v16, v1

    const/4 v1, 0x1

    .end local v16    # "unexpectedValues":Z
    .local v1, "unexpectedValues":Z
    goto :goto_6

    .end local v1    # "unexpectedValues":Z
    .restart local v16    # "unexpectedValues":Z
    :cond_5
    move-object v12, v0

    const/4 v1, 0x1

    goto :goto_6

    .line 142
    .end local v0    # "clientMaxWindowBits":Ljava/lang/Integer;
    .restart local v12    # "clientMaxWindowBits":Ljava/lang/Integer;
    :cond_6
    const-string v0, "client_no_context_takeover"

    const/4 v1, 0x1

    invoke-static {v4, v0, v1}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_9

    .line 143
    if-eqz v13, :cond_7

    const/16 v16, 0x1

    .line 144
    :cond_7
    if-eqz v20, :cond_8

    const/16 v16, 0x1

    .line 145
    :cond_8
    const/4 v0, 0x1

    move v13, v0

    const/4 v1, 0x1

    .end local v13    # "clientNoContextTakeover":Z
    .local v0, "clientNoContextTakeover":Z
    goto :goto_6

    .line 147
    .end local v0    # "clientNoContextTakeover":Z
    .restart local v13    # "clientNoContextTakeover":Z
    :cond_9
    const-string v0, "server_max_window_bits"

    const/4 v1, 0x1

    invoke-static {v4, v0, v1}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_d

    .line 148
    if-eqz v14, :cond_a

    const/16 v16, 0x1

    .line 149
    :cond_a
    if-eqz v20, :cond_b

    invoke-static/range {v20 .. v20}, Lkotlin/text/StringsKt;->toIntOrNull(Ljava/lang/String;)Ljava/lang/Integer;

    move-result-object v0

    goto :goto_5

    :cond_b
    const/4 v0, 0x0

    .line 150
    .end local v14    # "serverMaxWindowBits":Ljava/lang/Integer;
    .local v0, "serverMaxWindowBits":Ljava/lang/Integer;
    :goto_5
    if-nez v0, :cond_c

    const/4 v1, 0x1

    move-object v14, v0

    move/from16 v16, v1

    const/4 v1, 0x1

    .end local v16    # "unexpectedValues":Z
    .restart local v1    # "unexpectedValues":Z
    goto :goto_6

    .end local v1    # "unexpectedValues":Z
    .restart local v16    # "unexpectedValues":Z
    :cond_c
    move-object v14, v0

    const/4 v1, 0x1

    goto :goto_6

    .line 152
    .end local v0    # "serverMaxWindowBits":Ljava/lang/Integer;
    .restart local v14    # "serverMaxWindowBits":Ljava/lang/Integer;
    :cond_d
    const-string v0, "server_no_context_takeover"

    const/4 v1, 0x1

    invoke-static {v4, v0, v1}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_10

    .line 153
    if-eqz v15, :cond_e

    const/16 v16, 0x1

    .line 154
    :cond_e
    if-eqz v20, :cond_f

    const/16 v16, 0x1

    .line 155
    :cond_f
    const/4 v0, 0x1

    move v15, v0

    .end local v15    # "serverNoContextTakeover":Z
    .local v0, "serverNoContextTakeover":Z
    goto :goto_6

    .line 158
    .end local v0    # "serverNoContextTakeover":Z
    .restart local v15    # "serverNoContextTakeover":Z
    :cond_10
    const/4 v0, 0x1

    move/from16 v16, v0

    .line 160
    .end local v4    # "name":Ljava/lang/String;
    .end local v6    # "equals":I
    .end local v11    # "parameterEnd":I
    .end local v20    # "value":Ljava/lang/String;
    :goto_6
    nop

    .line 126
    move-object/from16 v0, p1

    move v4, v1

    move/from16 v1, v21

    const/16 v6, 0x3b

    goto/16 :goto_2

    .end local v21    # "extensionEnd":I
    .local v1, "extensionEnd":I
    :cond_11
    move/from16 v21, v1

    move v1, v4

    .end local v1    # "extensionEnd":I
    .restart local v21    # "extensionEnd":I
    move v11, v2

    goto :goto_7

    .line 165
    .end local v2    # "compressionEnabled":Z
    .end local v21    # "extensionEnd":I
    .restart local v1    # "extensionEnd":I
    .local v11, "compressionEnabled":Z
    :cond_12
    move/from16 v21, v1

    move v1, v4

    .end local v1    # "extensionEnd":I
    .restart local v21    # "extensionEnd":I
    const/4 v0, 0x1

    move/from16 v16, v0

    .line 167
    .end local v7    # "extensionTokenEnd":I
    .end local v10    # "extensionToken":Ljava/lang/String;
    .end local v21    # "extensionEnd":I
    :goto_7
    nop

    .line 114
    move-object/from16 v0, p1

    move v4, v1

    move-object/from16 v17, v3

    move v1, v5

    const/4 v2, 0x0

    goto/16 :goto_1

    .end local v3    # "header":Ljava/lang/String;
    .end local v5    # "pos":I
    .local v1, "pos":I
    .restart local v17    # "header":Ljava/lang/String;
    :cond_13
    move v5, v1

    move-object/from16 v3, v17

    .line 106
    .end local v1    # "pos":I
    .end local v17    # "header":Ljava/lang/String;
    :goto_8
    nop

    .end local v9    # "i":I
    add-int/lit8 v9, v9, 0x1

    move-object/from16 v0, p1

    const/4 v2, 0x0

    goto/16 :goto_0

    .line 171
    :cond_14
    new-instance v10, Lokhttp3/internal/ws/WebSocketExtensions;

    .line 172
    nop

    .line 173
    nop

    .line 174
    nop

    .line 175
    nop

    .line 176
    nop

    .line 177
    nop

    .line 171
    invoke-direct/range {v10 .. v16}, Lokhttp3/internal/ws/WebSocketExtensions;-><init>(ZLjava/lang/Integer;ZLjava/lang/Integer;ZZ)V

    return-object v10
.end method

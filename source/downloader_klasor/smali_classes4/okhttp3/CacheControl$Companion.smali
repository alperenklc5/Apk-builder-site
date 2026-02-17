.class public final Lokhttp3/CacheControl$Companion;
.super Ljava/lang/Object;
.source "CacheControl.kt"


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lokhttp3/CacheControl;
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
        "\u0000&\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\u0008\u0002\n\u0002\u0018\u0002\n\u0002\u0008\u0003\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0008\n\u0002\u0010\u000e\n\u0002\u0008\u0003\u0008\u0086\u0003\u0018\u00002\u00020\u0001B\u0007\u0008\u0002\u00a2\u0006\u0002\u0010\u0002J\u0010\u0010\u0006\u001a\u00020\u00042\u0006\u0010\u0007\u001a\u00020\u0008H\u0007J\u001e\u0010\t\u001a\u00020\n*\u00020\u000b2\u0006\u0010\u000c\u001a\u00020\u000b2\u0008\u0008\u0002\u0010\r\u001a\u00020\nH\u0002R\u0010\u0010\u0003\u001a\u00020\u00048\u0006X\u0087\u0004\u00a2\u0006\u0002\n\u0000R\u0010\u0010\u0005\u001a\u00020\u00048\u0006X\u0087\u0004\u00a2\u0006\u0002\n\u0000\u00a8\u0006\u000e"
    }
    d2 = {
        "Lokhttp3/CacheControl$Companion;",
        "",
        "()V",
        "FORCE_CACHE",
        "Lokhttp3/CacheControl;",
        "FORCE_NETWORK",
        "parse",
        "headers",
        "Lokhttp3/Headers;",
        "indexOfElement",
        "",
        "",
        "characters",
        "startIndex",
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

    .line 258
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public synthetic constructor <init>(Lkotlin/jvm/internal/DefaultConstructorMarker;)V
    .locals 0
    .param p1, "$constructor_marker"    # Lkotlin/jvm/internal/DefaultConstructorMarker;

    .line 258
    invoke-direct {p0}, Lokhttp3/CacheControl$Companion;-><init>()V

    return-void
.end method

.method private final indexOfElement(Ljava/lang/String;Ljava/lang/String;I)I
    .locals 7
    .param p1, "$this$indexOfElement"    # Ljava/lang/String;
    .param p2, "characters"    # Ljava/lang/String;
    .param p3, "startIndex"    # I

    .line 407
    invoke-virtual {p1}, Ljava/lang/String;->length()I

    move-result v0

    move v1, p3

    :goto_0
    if-ge v1, v0, :cond_1

    .line 408
    .local v1, "i":I
    move-object v2, p2

    check-cast v2, Ljava/lang/CharSequence;

    invoke-virtual {p1, v1}, Ljava/lang/String;->charAt(I)C

    move-result v3

    const/4 v4, 0x2

    const/4 v5, 0x0

    const/4 v6, 0x0

    invoke-static {v2, v3, v6, v4, v5}, Lkotlin/text/StringsKt;->contains$default(Ljava/lang/CharSequence;CZILjava/lang/Object;)Z

    move-result v2

    if-eqz v2, :cond_0

    .line 409
    return v1

    .line 407
    :cond_0
    nop

    .end local v1    # "i":I
    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    .line 412
    :cond_1
    invoke-virtual {p1}, Ljava/lang/String;->length()I

    move-result v0

    return v0
.end method

.method static synthetic indexOfElement$default(Lokhttp3/CacheControl$Companion;Ljava/lang/String;Ljava/lang/String;IILjava/lang/Object;)I
    .locals 0

    and-int/lit8 p4, p4, 0x2

    if-eqz p4, :cond_0

    .line 406
    const/4 p3, 0x0

    :cond_0
    invoke-direct {p0, p1, p2, p3}, Lokhttp3/CacheControl$Companion;->indexOfElement(Ljava/lang/String;Ljava/lang/String;I)I

    move-result p0

    return p0
.end method


# virtual methods
.method public final parse(Lokhttp3/Headers;)Lokhttp3/CacheControl;
    .locals 37
    .param p1, "headers"    # Lokhttp3/Headers;
    .annotation runtime Lkotlin/jvm/JvmStatic;
    .end annotation

    move-object/from16 v0, p1

    const-string v1, "headers"

    invoke-static {v0, v1}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullParameter(Ljava/lang/Object;Ljava/lang/String;)V

    .line 285
    const/4 v1, 0x0

    .line 286
    .local v1, "noCache":Z
    const/4 v2, 0x0

    .line 287
    .local v2, "noStore":Z
    const/4 v3, -0x1

    .line 288
    .local v3, "maxAgeSeconds":I
    const/4 v4, -0x1

    .line 289
    .local v4, "sMaxAgeSeconds":I
    const/4 v5, 0x0

    .line 290
    .local v5, "isPrivate":Z
    const/4 v6, 0x0

    .line 291
    .local v6, "isPublic":Z
    const/4 v7, 0x0

    .line 292
    .local v7, "mustRevalidate":Z
    const/4 v8, -0x1

    .line 293
    .local v8, "maxStaleSeconds":I
    const/4 v9, -0x1

    .line 294
    .local v9, "minFreshSeconds":I
    const/4 v10, 0x0

    .line 295
    .local v10, "onlyIfCached":Z
    const/4 v11, 0x0

    .line 296
    .local v11, "noTransform":Z
    const/4 v12, 0x0

    .line 298
    .local v12, "immutable":Z
    const/4 v13, 0x1

    .line 299
    .local v13, "canUseHeaderValue":Z
    const/4 v14, 0x0

    move-object v15, v14

    check-cast v15, Ljava/lang/String;

    .line 301
    .local v15, "headerValue":Ljava/lang/String;
    move-object/from16 v16, v14

    invoke-virtual {v0}, Lokhttp3/Headers;->size()I

    move-result v14

    const/16 v17, 0x0

    move/from16 v19, v1

    move/from16 v20, v2

    move/from16 v21, v3

    move/from16 v22, v4

    move/from16 v23, v5

    move/from16 v24, v6

    move/from16 v25, v7

    move/from16 v26, v8

    move/from16 v27, v9

    move/from16 v28, v10

    move/from16 v29, v11

    move/from16 v30, v12

    move/from16 v1, v17

    .end local v1    # "noCache":Z
    .end local v2    # "noStore":Z
    .end local v3    # "maxAgeSeconds":I
    .end local v4    # "sMaxAgeSeconds":I
    .end local v5    # "isPrivate":Z
    .end local v6    # "isPublic":Z
    .end local v7    # "mustRevalidate":Z
    .end local v8    # "maxStaleSeconds":I
    .end local v9    # "minFreshSeconds":I
    .end local v10    # "onlyIfCached":Z
    .end local v11    # "noTransform":Z
    .end local v12    # "immutable":Z
    .local v19, "noCache":Z
    .local v20, "noStore":Z
    .local v21, "maxAgeSeconds":I
    .local v22, "sMaxAgeSeconds":I
    .local v23, "isPrivate":Z
    .local v24, "isPublic":Z
    .local v25, "mustRevalidate":Z
    .local v26, "maxStaleSeconds":I
    .local v27, "minFreshSeconds":I
    .local v28, "onlyIfCached":Z
    .local v29, "noTransform":Z
    .local v30, "immutable":Z
    :goto_0
    if-ge v1, v14, :cond_18

    .line 302
    .local v1, "i":I
    invoke-virtual {v0, v1}, Lokhttp3/Headers;->name(I)Ljava/lang/String;

    move-result-object v2

    .line 303
    .local v2, "name":Ljava/lang/String;
    invoke-virtual {v0, v1}, Lokhttp3/Headers;->value(I)Ljava/lang/String;

    move-result-object v3

    .line 305
    .local v3, "value":Ljava/lang/String;
    nop

    .line 306
    const-string v4, "Cache-Control"

    const/4 v5, 0x1

    invoke-static {v2, v4, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v4

    if-eqz v4, :cond_1

    .line 307
    if-eqz v15, :cond_0

    .line 309
    const/4 v13, 0x0

    goto :goto_1

    .line 311
    :cond_0
    move-object v15, v3

    .line 312
    goto :goto_1

    .line 314
    :cond_1
    const-string v4, "Pragma"

    invoke-static {v2, v4, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v4

    if-eqz v4, :cond_16

    .line 316
    const/4 v13, 0x0

    .line 321
    :goto_1
    nop

    .line 323
    const/4 v4, 0x0

    .line 324
    .local v4, "pos":I
    :goto_2
    invoke-virtual {v3}, Ljava/lang/String;->length()I

    move-result v6

    if-ge v4, v6, :cond_17

    .line 325
    move v6, v4

    .line 326
    .local v6, "tokenStart":I
    move-object/from16 v7, p0

    check-cast v7, Lokhttp3/CacheControl$Companion;

    const-string v8, "=,;"

    invoke-direct {v7, v3, v8, v4}, Lokhttp3/CacheControl$Companion;->indexOfElement(Ljava/lang/String;Ljava/lang/String;I)I

    move-result v4

    .line 327
    const-string v7, "null cannot be cast to non-null type java.lang.String"

    if-eqz v3, :cond_15

    invoke-virtual {v3, v6, v4}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v8

    const-string v9, "(this as java.lang.Strin\u2026ing(startIndex, endIndex)"

    invoke-static {v8, v9}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullExpressionValue(Ljava/lang/Object;Ljava/lang/String;)V

    const-string v10, "null cannot be cast to non-null type kotlin.CharSequence"

    if-eqz v8, :cond_14

    check-cast v8, Ljava/lang/CharSequence;

    invoke-static {v8}, Lkotlin/text/StringsKt;->trim(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;

    move-result-object v8

    invoke-virtual {v8}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v8

    .line 328
    .local v8, "directive":Ljava/lang/String;
    const/4 v11, 0x0

    .line 330
    .local v11, "parameter":Ljava/lang/String;
    invoke-virtual {v3}, Ljava/lang/String;->length()I

    move-result v12

    if-eq v4, v12, :cond_7

    invoke-virtual {v3, v4}, Ljava/lang/String;->charAt(I)C

    move-result v12

    const/16 v5, 0x2c

    if-eq v12, v5, :cond_7

    invoke-virtual {v3, v4}, Ljava/lang/String;->charAt(I)C

    move-result v5

    const/16 v12, 0x3b

    if-ne v5, v12, :cond_2

    goto :goto_3

    .line 334
    :cond_2
    add-int/lit8 v4, v4, 0x1

    .line 335
    invoke-static {v3, v4}, Lokhttp3/internal/Util;->indexOfNonWhitespace(Ljava/lang/String;I)I

    move-result v4

    .line 337
    invoke-virtual {v3}, Ljava/lang/String;->length()I

    move-result v5

    if-ge v4, v5, :cond_4

    invoke-virtual {v3, v4}, Ljava/lang/String;->charAt(I)C

    move-result v5

    const/16 v12, 0x22

    if-ne v5, v12, :cond_4

    .line 339
    add-int/lit8 v33, v4, 0x1

    .line 340
    .end local v4    # "pos":I
    .local v33, "pos":I
    move/from16 v4, v33

    .line 341
    .local v4, "parameterStart":I
    move-object/from16 v31, v3

    check-cast v31, Ljava/lang/CharSequence;

    const/16 v35, 0x4

    const/16 v36, 0x0

    const/16 v32, 0x22

    const/16 v34, 0x0

    invoke-static/range {v31 .. v36}, Lkotlin/text/StringsKt;->indexOf$default(Ljava/lang/CharSequence;CIZILjava/lang/Object;)I

    move-result v5

    .line 342
    .end local v33    # "pos":I
    .local v5, "pos":I
    if-eqz v3, :cond_3

    invoke-virtual {v3, v4, v5}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v7

    invoke-static {v7, v9}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullExpressionValue(Ljava/lang/Object;Ljava/lang/String;)V

    .line 343
    .end local v11    # "parameter":Ljava/lang/String;
    .local v7, "parameter":Ljava/lang/String;
    nop

    .end local v4    # "parameterStart":I
    add-int/lit8 v5, v5, 0x1

    move v4, v5

    goto :goto_4

    .line 342
    .end local v7    # "parameter":Ljava/lang/String;
    .restart local v4    # "parameterStart":I
    .restart local v11    # "parameter":Ljava/lang/String;
    :cond_3
    new-instance v9, Ljava/lang/NullPointerException;

    invoke-direct {v9, v7}, Ljava/lang/NullPointerException;-><init>(Ljava/lang/String;)V

    throw v9

    .line 346
    .end local v5    # "pos":I
    .local v4, "pos":I
    :cond_4
    move v5, v4

    .line 347
    .local v5, "parameterStart":I
    move-object/from16 v12, p0

    check-cast v12, Lokhttp3/CacheControl$Companion;

    const-string v0, ",;"

    invoke-direct {v12, v3, v0, v4}, Lokhttp3/CacheControl$Companion;->indexOfElement(Ljava/lang/String;Ljava/lang/String;I)I

    move-result v0

    .line 348
    .end local v4    # "pos":I
    .local v0, "pos":I
    if-eqz v3, :cond_6

    invoke-virtual {v3, v5, v0}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v4

    invoke-static {v4, v9}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullExpressionValue(Ljava/lang/Object;Ljava/lang/String;)V

    if-eqz v4, :cond_5

    check-cast v4, Ljava/lang/CharSequence;

    invoke-static {v4}, Lkotlin/text/StringsKt;->trim(Ljava/lang/CharSequence;)Ljava/lang/CharSequence;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v7

    move v4, v0

    .end local v11    # "parameter":Ljava/lang/String;
    .restart local v7    # "parameter":Ljava/lang/String;
    goto :goto_4

    .end local v7    # "parameter":Ljava/lang/String;
    .restart local v11    # "parameter":Ljava/lang/String;
    :cond_5
    new-instance v4, Ljava/lang/NullPointerException;

    invoke-direct {v4, v10}, Ljava/lang/NullPointerException;-><init>(Ljava/lang/String;)V

    throw v4

    :cond_6
    new-instance v4, Ljava/lang/NullPointerException;

    invoke-direct {v4, v7}, Ljava/lang/NullPointerException;-><init>(Ljava/lang/String;)V

    throw v4

    .line 331
    .end local v0    # "pos":I
    .end local v5    # "parameterStart":I
    .restart local v4    # "pos":I
    :cond_7
    :goto_3
    add-int/lit8 v4, v4, 0x1

    .line 332
    move-object/from16 v7, v16

    check-cast v7, Ljava/lang/String;

    .line 349
    .end local v11    # "parameter":Ljava/lang/String;
    .restart local v7    # "parameter":Ljava/lang/String;
    :goto_4
    nop

    .line 350
    nop

    .line 352
    nop

    .line 353
    const-string v0, "no-cache"

    const/4 v5, 0x1

    invoke-static {v0, v8, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_8

    .line 354
    const/4 v0, 0x1

    move/from16 v19, v0

    .end local v19    # "noCache":Z
    .local v0, "noCache":Z
    goto/16 :goto_5

    .line 356
    .end local v0    # "noCache":Z
    .restart local v19    # "noCache":Z
    :cond_8
    const-string v0, "no-store"

    invoke-static {v0, v8, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_9

    .line 357
    const/4 v0, 0x1

    move/from16 v20, v0

    .end local v20    # "noStore":Z
    .local v0, "noStore":Z
    goto/16 :goto_5

    .line 359
    .end local v0    # "noStore":Z
    .restart local v20    # "noStore":Z
    :cond_9
    const-string v0, "max-age"

    invoke-static {v0, v8, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    const/4 v9, -0x1

    if-eqz v0, :cond_a

    .line 360
    invoke-static {v7, v9}, Lokhttp3/internal/Util;->toNonNegativeInt(Ljava/lang/String;I)I

    move-result v0

    move/from16 v21, v0

    .end local v21    # "maxAgeSeconds":I
    .local v0, "maxAgeSeconds":I
    goto/16 :goto_5

    .line 362
    .end local v0    # "maxAgeSeconds":I
    .restart local v21    # "maxAgeSeconds":I
    :cond_a
    const-string v0, "s-maxage"

    invoke-static {v0, v8, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_b

    .line 363
    invoke-static {v7, v9}, Lokhttp3/internal/Util;->toNonNegativeInt(Ljava/lang/String;I)I

    move-result v0

    move/from16 v22, v0

    .end local v22    # "sMaxAgeSeconds":I
    .local v0, "sMaxAgeSeconds":I
    goto/16 :goto_5

    .line 365
    .end local v0    # "sMaxAgeSeconds":I
    .restart local v22    # "sMaxAgeSeconds":I
    :cond_b
    const-string v0, "private"

    invoke-static {v0, v8, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_c

    .line 366
    const/4 v0, 0x1

    move/from16 v23, v0

    .end local v23    # "isPrivate":Z
    .local v0, "isPrivate":Z
    goto :goto_5

    .line 368
    .end local v0    # "isPrivate":Z
    .restart local v23    # "isPrivate":Z
    :cond_c
    const-string v0, "public"

    invoke-static {v0, v8, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_d

    .line 369
    const/4 v0, 0x1

    move/from16 v24, v0

    .end local v24    # "isPublic":Z
    .local v0, "isPublic":Z
    goto :goto_5

    .line 371
    .end local v0    # "isPublic":Z
    .restart local v24    # "isPublic":Z
    :cond_d
    const-string v0, "must-revalidate"

    invoke-static {v0, v8, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_e

    .line 372
    const/4 v0, 0x1

    move/from16 v25, v0

    .end local v25    # "mustRevalidate":Z
    .local v0, "mustRevalidate":Z
    goto :goto_5

    .line 374
    .end local v0    # "mustRevalidate":Z
    .restart local v25    # "mustRevalidate":Z
    :cond_e
    const-string v0, "max-stale"

    invoke-static {v0, v8, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_f

    .line 375
    const v0, 0x7fffffff

    invoke-static {v7, v0}, Lokhttp3/internal/Util;->toNonNegativeInt(Ljava/lang/String;I)I

    move-result v0

    move/from16 v26, v0

    .end local v26    # "maxStaleSeconds":I
    .local v0, "maxStaleSeconds":I
    goto :goto_5

    .line 377
    .end local v0    # "maxStaleSeconds":I
    .restart local v26    # "maxStaleSeconds":I
    :cond_f
    const-string v0, "min-fresh"

    invoke-static {v0, v8, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_10

    .line 378
    invoke-static {v7, v9}, Lokhttp3/internal/Util;->toNonNegativeInt(Ljava/lang/String;I)I

    move-result v0

    move/from16 v27, v0

    .end local v27    # "minFreshSeconds":I
    .local v0, "minFreshSeconds":I
    goto :goto_5

    .line 380
    .end local v0    # "minFreshSeconds":I
    .restart local v27    # "minFreshSeconds":I
    :cond_10
    const-string v0, "only-if-cached"

    invoke-static {v0, v8, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_11

    .line 381
    const/4 v0, 0x1

    move/from16 v28, v0

    .end local v28    # "onlyIfCached":Z
    .local v0, "onlyIfCached":Z
    goto :goto_5

    .line 383
    .end local v0    # "onlyIfCached":Z
    .restart local v28    # "onlyIfCached":Z
    :cond_11
    const-string v0, "no-transform"

    invoke-static {v0, v8, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_12

    .line 384
    const/4 v0, 0x1

    move/from16 v29, v0

    .end local v29    # "noTransform":Z
    .local v0, "noTransform":Z
    goto :goto_5

    .line 386
    .end local v0    # "noTransform":Z
    .restart local v29    # "noTransform":Z
    :cond_12
    const-string v0, "immutable"

    invoke-static {v0, v8, v5}, Lkotlin/text/StringsKt;->equals(Ljava/lang/String;Ljava/lang/String;Z)Z

    move-result v0

    if-eqz v0, :cond_13

    .line 387
    const/4 v0, 0x1

    move/from16 v30, v0

    .line 389
    .end local v6    # "tokenStart":I
    .end local v7    # "parameter":Ljava/lang/String;
    .end local v8    # "directive":Ljava/lang/String;
    :cond_13
    :goto_5
    nop

    .line 324
    move-object/from16 v0, p1

    goto/16 :goto_2

    .line 327
    .restart local v6    # "tokenStart":I
    :cond_14
    new-instance v0, Ljava/lang/NullPointerException;

    invoke-direct {v0, v10}, Ljava/lang/NullPointerException;-><init>(Ljava/lang/String;)V

    throw v0

    :cond_15
    new-instance v0, Ljava/lang/NullPointerException;

    invoke-direct {v0, v7}, Ljava/lang/NullPointerException;-><init>(Ljava/lang/String;)V

    throw v0

    .line 319
    .end local v4    # "pos":I
    .end local v6    # "tokenStart":I
    :cond_16
    nop

    .line 301
    .end local v2    # "name":Ljava/lang/String;
    .end local v3    # "value":Ljava/lang/String;
    :cond_17
    nop

    .end local v1    # "i":I
    add-int/lit8 v1, v1, 0x1

    move-object/from16 v0, p1

    goto/16 :goto_0

    .line 393
    :cond_18
    if-nez v13, :cond_19

    .line 394
    move-object/from16 v15, v16

    check-cast v15, Ljava/lang/String;

    move-object/from16 v31, v15

    goto :goto_6

    .line 393
    :cond_19
    move-object/from16 v31, v15

    .line 397
    .end local v15    # "headerValue":Ljava/lang/String;
    .local v31, "headerValue":Ljava/lang/String;
    :goto_6
    new-instance v18, Lokhttp3/CacheControl;

    .line 398
    nop

    .line 399
    nop

    .line 397
    const/16 v32, 0x0

    invoke-direct/range {v18 .. v32}, Lokhttp3/CacheControl;-><init>(ZZIIZZZIIZZZLjava/lang/String;Lkotlin/jvm/internal/DefaultConstructorMarker;)V

    return-object v18
.end method

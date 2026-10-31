module.exports = [
(()=>{"use strict";return[
"[project]/src/app/favicon.ico.mjs { IMAGE => \"[project]/src/app/favicon.ico (static in ecmascript, tag client)\" } [app-rsc] (structured image object, ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>__TURBOPACK__default__export__
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$app$2f$favicon$2e$ico__$28$static__in__ecmascript$2c$__tag__client$29$__ = __turbopack_context__.i("[project]/src/app/favicon.ico (static in ecmascript, tag client)");
;
const __TURBOPACK__default__export__ = {
    src: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$app$2f$favicon$2e$ico__$28$static__in__ecmascript$2c$__tag__client$29$__["default"],
    width: 256,
    height: 256
};
}),
"[project]/src/app/page.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Home,
    "dynamic",
    ()=>dynamic
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-jsx-dev-runtime.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$image$2d$component$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__Image__as__default$3e$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/image-component.js [app-rsc] (ecmascript) <export Image as default>");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$fanvue$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/fanvue.ts [app-rsc] (ecmascript)");
;
;
;
const dynamic = "force-dynamic";
async function Home({ searchParams }) {
    const me = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$fanvue$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["getCurrentUser"])();
    const isAuthed = !!me;
    const params = await searchParams;
    const errorParam = typeof params?.error === "string" ? params.error : undefined;
    const errorDescriptionParam = typeof params?.error_description === "string" ? params.error_description : undefined;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
                className: "flex flex-col gap-[24px] row-start-2 items-center sm:items-start max-w-[720px] w-full",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$image$2d$component$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__Image__as__default$3e$__["default"], {
                        src: "/logo192.png",
                        alt: "Fanvue",
                        width: 180,
                        height: 38,
                        priority: true
                    }, void 0, false, {
                        fileName: "[project]/src/app/page.tsx",
                        lineNumber: 15,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "w-full rounded-lg border border-black/[.08] dark:border-white/[.145] p-4 sm:p-6",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "flex items-center justify-between gap-4",
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                        className: "font-semibold text-lg",
                                        children: "Fanvue App Starter"
                                    }, void 0, false, {
                                        fileName: "[project]/src/app/page.tsx",
                                        lineNumber: 24,
                                        columnNumber: 13
                                    }, this),
                                    isAuthed ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("form", {
                                        action: "/api/oauth/logout",
                                        method: "post",
                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            className: "rounded-full border border-solid border-transparent transition-colors bg-[#49f264ff] hover:bg-[#49f26433] text-black px-4 h-10 flex items-center gap-2 cursor-pointer hover:text-white group",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
                                                    "aria-hidden": true,
                                                    width: "20",
                                                    height: "20",
                                                    viewBox: "0 0 24 24",
                                                    fill: "none",
                                                    xmlns: "http://www.w3.org/2000/svg",
                                                    className: "text-black group-hover:text-white transition-colors",
                                                    children: [
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                                                            d: "m16 17 5-5-5-5",
                                                            stroke: "currentColor",
                                                            strokeWidth: "2",
                                                            strokeLinecap: "round",
                                                            strokeLinejoin: "round"
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/app/page.tsx",
                                                            lineNumber: 37,
                                                            columnNumber: 21
                                                        }, this),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                                                            d: "M21 12H9",
                                                            stroke: "currentColor",
                                                            strokeWidth: "2",
                                                            strokeLinecap: "round",
                                                            strokeLinejoin: "round"
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/app/page.tsx",
                                                            lineNumber: 38,
                                                            columnNumber: 21
                                                        }, this),
                                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                                                            d: "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4",
                                                            stroke: "currentColor",
                                                            strokeWidth: "2",
                                                            strokeLinecap: "round",
                                                            strokeLinejoin: "round"
                                                        }, void 0, false, {
                                                            fileName: "[project]/src/app/page.tsx",
                                                            lineNumber: 39,
                                                            columnNumber: 21
                                                        }, this)
                                                    ]
                                                }, void 0, true, {
                                                    fileName: "[project]/src/app/page.tsx",
                                                    lineNumber: 28,
                                                    columnNumber: 19
                                                }, this),
                                                "Logout"
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/src/app/page.tsx",
                                            lineNumber: 27,
                                            columnNumber: 17
                                        }, this)
                                    }, void 0, false, {
                                        fileName: "[project]/src/app/page.tsx",
                                        lineNumber: 26,
                                        columnNumber: 15
                                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                                        className: "rounded-full border border-solid border-transparent transition-colors bg-[#49f264ff] hover:bg-[#49f26433] text-black hover:text-white px-4 h-10 flex items-center gap-2 cursor-pointer",
                                        href: "/api/oauth/login",
                                        target: "_top",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$image$2d$component$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__Image__as__default$3e$__["default"], {
                                                "aria-hidden": true,
                                                src: "/logo192.png",
                                                alt: "",
                                                width: 20,
                                                height: 20
                                            }, void 0, false, {
                                                fileName: "[project]/src/app/page.tsx",
                                                lineNumber: 50,
                                                columnNumber: 17
                                            }, this),
                                            "Login with Fanvue"
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/app/page.tsx",
                                        lineNumber: 45,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/app/page.tsx",
                                lineNumber: 23,
                                columnNumber: 11
                            }, this),
                            !isAuthed && (errorParam || errorDescriptionParam) ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "mt-3 text-sm text-red-600",
                                children: errorDescriptionParam || errorParam
                            }, void 0, false, {
                                fileName: "[project]/src/app/page.tsx",
                                lineNumber: 56,
                                columnNumber: 13
                            }, this) : null,
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "mt-4",
                                children: isAuthed ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                                    className: "text-xs overflow-auto p-3 rounded bg-black/[.05] dark:bg-white/[.06]",
                                    children: JSON.stringify(me, null, 2)
                                }, void 0, false, {
                                    fileName: "[project]/src/app/page.tsx",
                                    lineNumber: 62,
                                    columnNumber: 15
                                }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                    className: "text-sm text-black/70 dark:text-white/70",
                                    children: 'Click "Login with Fanvue" to authenticate and we will display your current user from the Fanvue API.'
                                }, void 0, false, {
                                    fileName: "[project]/src/app/page.tsx",
                                    lineNumber: 64,
                                    columnNumber: 15
                                }, this)
                            }, void 0, false, {
                                fileName: "[project]/src/app/page.tsx",
                                lineNumber: 60,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/app/page.tsx",
                        lineNumber: 22,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 14,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("footer", {
                className: "row-start-3 flex gap-[24px] flex-wrap items-center justify-center",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                        className: "flex items-center gap-2 hover:underline hover:underline-offset-4",
                        href: "https://api.fanvue.com/docs",
                        target: "_blank",
                        rel: "noopener noreferrer",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$image$2d$component$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__Image__as__default$3e$__["default"], {
                                "aria-hidden": true,
                                src: "/file.svg",
                                alt: "Docs icon",
                                width: 16,
                                height: 16
                            }, void 0, false, {
                                fileName: "[project]/src/app/page.tsx",
                                lineNumber: 78,
                                columnNumber: 11
                            }, this),
                            "Fanvue API Docs"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/app/page.tsx",
                        lineNumber: 72,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                        className: "flex items-center gap-2 hover:underline hover:underline-offset-4",
                        href: "https://fanvue.com",
                        target: "_blank",
                        rel: "noopener noreferrer",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$image$2d$component$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__Image__as__default$3e$__["default"], {
                                "aria-hidden": true,
                                src: "/globe.svg",
                                alt: "Website icon",
                                width: 16,
                                height: 16
                            }, void 0, false, {
                                fileName: "[project]/src/app/page.tsx",
                                lineNumber: 93,
                                columnNumber: 11
                            }, this),
                            "Visit fanvue.com →"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/app/page.tsx",
                        lineNumber: 87,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/page.tsx",
                lineNumber: 71,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/app/page.tsx",
        lineNumber: 13,
        columnNumber: 5
    }, this);
}
}),
"[project]/src/env.ts [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "env",
    ()=>env,
    "oauthConfig",
    ()=>oauthConfig
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$t3$2d$oss$2f$env$2d$nextjs$2f$dist$2f$index$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/@t3-oss/env-nextjs/dist/index.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$string$3e$__ = __turbopack_context__.i("[project]/node_modules/zod/v4/classic/external.js [app-rsc] (ecmascript) <export * as z .string>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$url$3e$__ = __turbopack_context__.i("[project]/node_modules/zod/v4/classic/external.js [app-rsc] (ecmascript) <export * as z .url>");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$enum$3e$__ = __turbopack_context__.i("[project]/node_modules/zod/v4/classic/external.js [app-rsc] (ecmascript) <export * as z .enum>");
;
;
const env = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$t3$2d$oss$2f$env$2d$nextjs$2f$dist$2f$index$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["createEnv"])({
    server: {
        OAUTH_CLIENT_ID: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$string$3e$__["z"].string().min(1),
        OAUTH_CLIENT_SECRET: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$string$3e$__["z"].string().min(1),
        OAUTH_ISSUER_BASE_URL: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$url$3e$__["z"].url().default("https://auth.fanvue.com"),
        OAUTH_REDIRECT_URI: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$url$3e$__["z"].url().optional(),
        OAUTH_SCOPES: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$string$3e$__["z"].string(),
        OAUTH_RESPONSE_MODE: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$enum$3e$__["z"].enum([
            "query",
            "form_post"
        ]).optional(),
        OAUTH_PROMPT: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$string$3e$__["z"].string().optional(),
        BASE_URL: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$url$3e$__["z"].url().optional(),
        SESSION_COOKIE_NAME: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$string$3e$__["z"].string().default("fanvue_oauth"),
        SESSION_SECRET: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$string$3e$__["z"].string().min(16, {
            message: "SESSION_SECRET must be at least 32 characters"
        }),
        API_BASE_URL: __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zod$2f$v4$2f$classic$2f$external$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$export__$2a$__as__z__$2e$url$3e$__["z"].url().default("https://api.fanvue.com")
    },
    runtimeEnv: {
        OAUTH_CLIENT_ID: process.env.OAUTH_CLIENT_ID,
        OAUTH_CLIENT_SECRET: process.env.OAUTH_CLIENT_SECRET,
        OAUTH_ISSUER_BASE_URL: process.env.OAUTH_ISSUER_BASE_URL,
        OAUTH_REDIRECT_URI: process.env.OAUTH_REDIRECT_URI,
        OAUTH_SCOPES: process.env.OAUTH_SCOPES,
        OAUTH_RESPONSE_MODE: process.env.OAUTH_RESPONSE_MODE,
        OAUTH_PROMPT: process.env.OAUTH_PROMPT,
        BASE_URL: process.env.BASE_URL,
        SESSION_COOKIE_NAME: process.env.SESSION_COOKIE_NAME,
        SESSION_SECRET: process.env.SESSION_SECRET,
        API_BASE_URL: process.env.API_BASE_URL
    },
    emptyStringAsUndefined: true
});
const oauthConfig = {
    issuerBaseURL: env.OAUTH_ISSUER_BASE_URL,
    clientId: env.OAUTH_CLIENT_ID,
    clientSecret: env.OAUTH_CLIENT_SECRET,
    redirectUri: env.OAUTH_REDIRECT_URI
};
}),
"[project]/src/lib/fanvue.ts [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "getCurrentUser",
    ()=>getCurrentUser
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/env.ts [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$session$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/session.ts [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$oauth$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/oauth.ts [app-rsc] (ecmascript)");
;
;
;
async function getCurrentUser() {
    let session = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$session$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["getSession"])();
    if (!session) return null;
    if (Date.now() >= session.expiresAt - 30_000 && session.refreshToken) {
        try {
            const refreshed = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$oauth$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["refreshAccessToken"])(session.refreshToken);
            const updatedSession = {
                accessToken: refreshed.access_token,
                refreshToken: refreshed.refresh_token ?? session.refreshToken,
                tokenType: refreshed.token_type,
                scope: refreshed.scope ?? session.scope,
                expiresAt: Date.now() + refreshed.expires_in * 1000
            };
            await (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$session$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["setSession"])(updatedSession);
            session = updatedSession;
        } catch  {}
    }
    try {
        const res = await fetch(`${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["env"].API_BASE_URL}/users/me`, {
            headers: {
                Authorization: `Bearer ${session.accessToken}`
            },
            cache: "no-store"
        });
        if (!res.ok) return null;
        return res.json();
    } catch (error) {
        console.log("error", error);
        return null;
    }
}
}),
"[project]/src/lib/oauth.ts [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "exchangeCodeForToken",
    ()=>exchangeCodeForToken,
    "generatePkce",
    ()=>generatePkce,
    "getAuthorizeUrl",
    ()=>getAuthorizeUrl,
    "refreshAccessToken",
    ()=>refreshAccessToken
]);
var __TURBOPACK__imported__module__$5b$externals$5d2f$crypto__$5b$external$5d$__$28$crypto$2c$__cjs$29$__ = __turbopack_context__.i("[externals]/crypto [external] (crypto, cjs)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/env.ts [app-rsc] (ecmascript)");
;
;
function base64url(input) {
    return input.toString("base64").replace(/=/g, "").replace(/\+/g, "-").replace(/\//g, "_");
}
function generatePkce() {
    const verifier = base64url((0, __TURBOPACK__imported__module__$5b$externals$5d2f$crypto__$5b$external$5d$__$28$crypto$2c$__cjs$29$__["randomBytes"])(32));
    const challenge = base64url((0, __TURBOPACK__imported__module__$5b$externals$5d2f$crypto__$5b$external$5d$__$28$crypto$2c$__cjs$29$__["createHash"])("sha256").update(verifier).digest());
    return {
        verifier,
        challenge,
        method: "S256"
    };
}
// Do not remove these, your app won't work without them
const DEFAULT_SCOPES = "openid offline_access offline";
function getAuthorizeUrl({ state, codeChallenge, redirectUri }) {
    const params = new URLSearchParams({
        response_type: "code",
        client_id: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["oauthConfig"].clientId,
        redirect_uri: redirectUri ?? __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["env"].OAUTH_REDIRECT_URI ?? __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["oauthConfig"].redirectUri ?? "",
        scope: `${DEFAULT_SCOPES} ${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["env"].OAUTH_SCOPES ?? ""}`,
        state,
        code_challenge: codeChallenge,
        code_challenge_method: "S256"
    });
    if (__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["env"].OAUTH_RESPONSE_MODE) params.set("response_mode", __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["env"].OAUTH_RESPONSE_MODE);
    // Force login prompt to allow switching accounts
    params.set("prompt", __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["env"].OAUTH_PROMPT || "login");
    return `${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["oauthConfig"].issuerBaseURL}/oauth2/auth?${params.toString()}`;
}
async function exchangeCodeForToken({ code, codeVerifier, redirectUri }) {
    const params = new URLSearchParams({
        grant_type: "authorization_code",
        code,
        redirect_uri: redirectUri ?? __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["oauthConfig"].redirectUri ?? "",
        client_id: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["oauthConfig"].clientId,
        code_verifier: codeVerifier
    });
    const res = await fetch(`${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["oauthConfig"].issuerBaseURL}/oauth2/token`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Authorization: "Basic " + Buffer.from(`${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["oauthConfig"].clientId}:${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["oauthConfig"].clientSecret}`).toString("base64")
        },
        body: params.toString()
    });
    if (!res.ok) {
        const text = await res.text();
        throw new Error(`Token exchange failed: ${res.status} ${text}`);
    }
    return await res.json();
}
async function refreshAccessToken(refreshToken) {
    const params = new URLSearchParams({
        grant_type: "refresh_token",
        refresh_token: refreshToken,
        client_id: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["oauthConfig"].clientId
    });
    const res = await fetch(`${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["oauthConfig"].issuerBaseURL}/oauth2/token`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            Authorization: "Basic " + Buffer.from(`${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["oauthConfig"].clientId}:${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["oauthConfig"].clientSecret}`).toString("base64")
        },
        body: params.toString()
    });
    if (!res.ok) {
        const text = await res.text();
        throw new Error(`Token refresh failed: ${res.status} ${text}`);
    }
    return await res.json();
}
}),
"[project]/src/lib/session.ts [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "clearSession",
    ()=>clearSession,
    "getSession",
    ()=>getSession,
    "setSession",
    ()=>setSession
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$headers$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/headers.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$jose$2f$dist$2f$webapi$2f$jwt$2f$sign$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/jose/dist/webapi/jwt/sign.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$jose$2f$dist$2f$webapi$2f$jwt$2f$verify$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/jose/dist/webapi/jwt/verify.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/env.ts [app-rsc] (ecmascript)");
;
;
;
const encoder = new TextEncoder();
const secretKey = encoder.encode(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["env"].SESSION_SECRET);
async function setSession(payload) {
    const jwt = await new __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$jose$2f$dist$2f$webapi$2f$jwt$2f$sign$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["SignJWT"](payload).setProtectedHeader({
        alg: "HS256"
    }).setIssuedAt().setExpirationTime("30d").sign(secretKey);
    const cookieStore = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$headers$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["cookies"])();
    cookieStore.set(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["env"].SESSION_COOKIE_NAME, jwt, {
        httpOnly: true,
        secure: ("TURBOPACK compile-time value", "development") === "production",
        sameSite: "lax",
        path: "/",
        maxAge: 60 * 60 * 24 * 30
    });
}
async function getSession() {
    const cookieStore = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$headers$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["cookies"])();
    const token = cookieStore.get(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["env"].SESSION_COOKIE_NAME)?.value;
    if (!token) return null;
    try {
        const { payload } = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$jose$2f$dist$2f$webapi$2f$jwt$2f$verify$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jwtVerify"])(token, secretKey);
        return payload;
    } catch  {
        return null;
    }
}
async function clearSession() {
    const cookieStore = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$headers$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["cookies"])();
    cookieStore.delete(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$env$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["env"].SESSION_COOKIE_NAME);
}
}),
]})(),
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
"[project]/src/app/favicon.ico (static in ecmascript, tag client)", ((__turbopack_context__) => {

__turbopack_context__.v("/_next/static/media/favicon.2vob68tjqpejf.ico" + (globalThis["NEXT_CLIENT_ASSET_SUFFIX"] || ''));}),
"[project]/src/app/page.tsx [app-rsc] (ecmascript, Next.js Server Component)", (function(__turbopack_context__){

__turbopack_context__.n(__turbopack_context__.i("[project]/src/app/page.tsx [app-rsc] (ecmascript)"));
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__02iau453qj6i5._.js.map
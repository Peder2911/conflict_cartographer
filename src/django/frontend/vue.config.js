
module.exports = {
  
   publicPath: "/static/",
   outputDir: './dist/',

   lintOnSave: "warning",
   filenameHashing: false,

   css: {
      extract: false,
   },

   configureWebpack: {
      optimization:{
         splitChunks: false
      },
      devServer: {
         public: "http://0.0.0.0:1337",
         host: "0.0.0.0",
         port: 1337,
         watchOptions: {
            poll : 1000
         },
         https: false,
         headers: {
            "Access-Control-Allow-Origin":  "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
            "Access-Control-Allow-Headers": "X-Requested-With, content-type, Authorization"
         },
         proxy: {
            "^/api": {
               target:       "http://localhost:8000/",
               changeOrigin: true,
               secure:       false,
               logLevel:     "debug",
            }
         }
   },

   },

   chainWebpack: config => {
      config.entry("accounts")
         .add("./src/accounts.js")
         .end()
   },
   runtimeCompiler: true
   };

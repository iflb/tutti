module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
       ? '/vue/' : '/vue-dev/',
    //outputDir: "/var/www/html/vue-dist",
    devServer: {
        //port: 8081,
        port: 80,
        public: process.env.DOMAIN_NAME,
        //publicPath: "/vue-dev/",
    },
    configureWebpack: {
        resolve: { symlinks: false },
        watch: true,
        watchOptions: {
            aggregateTimeout: 1000,
            poll: 5000
        },
        devServer: {
            watchOptions: {
                poll: true
            }
        }
    }
};


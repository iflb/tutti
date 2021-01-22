module.exports = {
    transpileDependencies: [ "vuetify" ],
    publicPath: process.env.NODE_ENV === 'production' ? '/vue/' : '/vue-dev/',
    devServer: {
        port: 80,
        public: process.env.DOMAIN_NAME,
    },
    configureWebpack: {
        resolve: { symlinks: false },
        watch: true,
        watchOptions: {
            aggregateTimeout: 1000,
            poll: 5000,
            ignored: /node_modules/
        },
        devServer: {
            watchOptions: {
                poll: true
            }
        },
        //optimization: {
        //    splitChunks: {
        //        minSize: 10000,
        //        maxSize: 250000,
        //    }
        //}
    }
};


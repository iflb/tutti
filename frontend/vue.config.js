module.exports = {
    publicPath: "/vue/",
    outputDir: "/var/www/html/vue-dist",
    devServer: {
        //port: 8081,
        port: 80,
        public: "ec2-mturk10-bak.r9n.net",
        publicPath: "/vue/",
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


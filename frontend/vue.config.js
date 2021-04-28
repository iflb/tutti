module.exports = {
    publicPath: '/',
    devServer: {
        port: 80,
        public:  process.env.NODE_ENV === 'production' ? process.env.VUE_APP_HOST : process.env.VUE_APP_DEV_HOST,
    },
    outputDir: 'dist/dist',
    configureWebpack: {
        resolve: { symlinks: false },
        devtool: 'source-map',
        devServer: {
            watchOptions: {
                poll: true
            }
        },
    }
};

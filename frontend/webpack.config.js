const webpack = require('webpack'); //to access built-in plugins

module.exports = {
    entry: {
        trainer: './app/trainer.js',
    },
    output: {
        filename: 'bundle_[name].js',
        path: './static/js'
    },
    module: {
//        loaders: [
//            { test: /\.css$/, use: [ 'style-loader', 'css-loader' ] },
//            { test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: "file-loader" },
//            { test: /\.(woff|woff2)$/, loader:"url-loader?prefix=font/&limit=5000" },
//            { test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: "url-loader?limit=10000&mimetype=application/octet-stream" },
//            { test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: "url-loader?limit=10000&mimetype=image/svg+xml" }
//        ],
        rules: [
            {
                test: /\.(js|jsx)$/, 
                exclude: '/node-modules/', 
                loader: "babel-loader",
                options: { presets: ['es2015', 'react']}
            },
            {
                test: /\.less$/,
                use: [
                    'style-loader',
                    { loader: 'css-loader', options: { importLoaders: 1 } },
                    'less-loader'
                ]
            },
            { test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: "file-loader" },
            { test: /\.(woff|woff2)$/, loader:"url-loader?prefix=font/&limit=5000" },
            { test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: "url-loader?limit=10000&mimetype=application/octet-stream" },
            { test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: "url-loader?limit=10000&mimetype=image/svg+xml" }
        ]
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env':{
                'NODE_ENV': JSON.stringify('development')
            }
        }),
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery"
        }),
        new webpack.optimize.UglifyJsPlugin({
            compress:{
                warnings: false 
            },
            sourceMap: true
        }),
    ],
    devtool: "source-map"
}


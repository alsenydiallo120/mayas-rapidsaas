/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'class',
    content: [
        './src/{{ app_name }}/templates/*.html',
        './src/{{ app_name }}/templates/**/*.html',
        './src/{{ app_name }}/templates/**/**/*.html',
        './node_modules/flowbite/**/*.js'
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    "50": "#eefaf5",
                    "100": "#c5f0e2",
                    "200": "#8be4cb",
                    "300": "#5cd5b6",
                    "400": "#2ac8a3",
                    "500": "#00b98e",
                    "600": "#009670",
                    "700": "#007358",
                    "800": "#005040",
                    "900": "#003729"
                },
                gray: {
                    "50": "#f7f7f9",
                    "100": "#e3e4e8",
                    "200": "#c8c9d1",
                    "300": "#a8a9b3",
                    "400": "#8a8b96",
                    "500": "#6d6f7a",
                    "600": "#525360",
                    "700": "#3c3d47",
                    "800": "#28292f",
                    "900": "#1a1b1e"
                }
            },
        },
        fontFamily: {
            'body': [
                'Inter',
                'ui-sans-serif',
                'system-ui',
                '-apple-system',
                'system-ui',
                'Segoe UI',
                'Roboto',
                'Helvetica Neue',
                'Arial',
                'Noto Sans',
                'sans-serif',
                'Apple Color Emoji',
                'Segoe UI Emoji',
                'Segoe UI Symbol',
                'Noto Color Emoji'
            ],
            'sans': [
                'Inter',
                'ui-sans-serif',
                'system-ui',
                '-apple-system',
                'system-ui',
                'Segoe UI',
                'Roboto',
                'Helvetica Neue',
                'Arial',
                'Noto Sans',
                'sans-serif',
                'Apple Color Emoji',
                'Segoe UI Emoji',
                'Segoe UI Symbol',
                'Noto Color Emoji'
            ]
        }
    },
    plugins: [
        require('flowbite/plugin')
    ],
}



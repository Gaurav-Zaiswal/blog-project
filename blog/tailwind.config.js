module.exports = {
    purge: [
        './templates/*.html',
        './templates/**/*.html',
    ],
    theme: {
        fontFamily: {
            display: ['Gilroy', 'sans-serif'],
            body: ['Gilroy', 'sans-serif'],

            priHeader: ['Gilroy', 'sans-serif'],
            secHeader: ['Graphik', 'sans-serif'],
            priBody: ["-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "Oxygen-Sans", "Ubuntu", "Cantarell", "Helvetica Neue", "sans-serif"],
            secBody: ['Poppins', 'sans-serif'],

        },
        extend: {},
    },
    variants: {
        textColor: ['responsive', 'hover', 'focus', 'active'],
        backgroundColor: ['responsive', 'hover', 'focus', 'active'],
    },
    plugins: [],
}

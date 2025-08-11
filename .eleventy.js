module.exports = function (eleventyConfig) {
    // statiska tillgångar (justera om dina mappar heter annat)
    eleventyConfig.addPassthroughCopy("css");
    eleventyConfig.addPassthroughCopy("images");
    eleventyConfig.addPassthroughCopy("style.css");

    return {
        dir: {
            input: ".",         // källmapp
            includes: "_includes",
            data: "_data",
            output: "site"      // välj "site" för tydlighet
        },
        templateFormats: ["html", "md", "liquid", "njk"],
        htmlTemplateEngine: "liquid",
        markdownTemplateEngine: "liquid"
    };
};

export function languageToCountry(url: string): string | null {
    try {
        const urlObj = new URL(url);
        const pathParts = urlObj.pathname.split('/');
        const postID = pathParts[pathParts.length - 2]; // Assuming it's always the second-to-last part

        return postID;
    } catch (error) {
        console.error("Invalid URL:", error);
        return null;
    }
}


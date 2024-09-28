export enum Language {
    English = "english",
    Hebrew = "hebrew",
    Original = "original",
}

export const languageToCountryCode = {
    [Language.English]: "US",   // United States
    [Language.Hebrew]: "IL",    // Israel
    [Language.Original]: "ZZ",  // Placeholder for "original" or unspecified language
};

export type Message = {
    id: number;
    title: string;
    message: string;
    link: string;
    media_url: string;
    username: string;
    english: string;
    hebrew: string;
    date: number;
};

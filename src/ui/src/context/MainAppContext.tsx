import { createContext, useState } from "react";

import { Language } from "../types";
import { PaginationContextProps } from "./interfaces/Pagination";
import { SelectedLanguageContextProps } from "./interfaces/SelectedLanguage";
import { ShowMediaContextProps } from "./interfaces/ShowMedia";
import { QueryContextProps } from "./interfaces/Query";

interface MainAppContext
    extends PaginationContextProps,
        QueryContextProps,
        SelectedLanguageContextProps,
        ShowMediaContextProps {}

export const MainAppContext = createContext<MainAppContext>({
    // Language
    selectedLanguage: Language.Original,
    setSelectedLanguage: () => {},

    // Pagination
    totalPageCount: 0,
    currentPage: 1,
    pageSize: 10,

    setCurrentPage: () => {},
    setPageSize: () => {},
    setTotalPageCount: () => {},

    // Query
    query: "",

    setQuery: () => {},

    // Show Media
    showMedia: true,

    setShowMedia: () => {},
});

interface MainAppProviderProps {
    children: React.ReactNode;
}

export const MainAppProvider: React.FC<MainAppProviderProps> = ({ children }) => {
    // Language
    const [currentPage, setCurrentPage] = useState<number>(1);
    const [pageSize, setPageSize] = useState<number>(10);
    const [totalPageCount, setTotalPageCount] = useState<number>(0);

    // Pagination
    const [selectedLanguage, setSelectedLanguage] = useState<Language>(Language.Original);

    // Query
    const [query, setQuery] = useState<string>("");

    // ShowMedia
    const [showMedia, setShowMedia] = useState<boolean>(true);

    return (
        <MainAppContext.Provider
            value={{
                // States
                currentPage,
                pageSize,
                query,
                selectedLanguage,
                showMedia,
                totalPageCount,
                // Setters
                setCurrentPage,
                setPageSize,
                setQuery,
                setSelectedLanguage,
                setShowMedia,
                setTotalPageCount,
            }}
        >
            {children}
        </MainAppContext.Provider>
    );
};

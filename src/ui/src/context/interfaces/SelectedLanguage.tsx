import { Language } from "../../types";

export interface SelectedLanguageContextProps {
    selectedLanguage: Language;
    setSelectedLanguage(language: Language): void;
}

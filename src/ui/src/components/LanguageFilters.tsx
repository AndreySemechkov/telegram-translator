import { Button } from "antd";
import { isMobile } from "react-device-detect";
import { QuestionOutlined } from "@ant-design/icons";
import getUnicodeFlagIcon from "country-flag-icons/unicode";
import React, { useContext } from "react";

import { Language, languageToCountryCode } from "../types";
import { MainAppContext } from "../context/MainAppContext";

const Buttons = () => {
    const { selectedLanguage, setSelectedLanguage } = useContext(MainAppContext);

    return Object.values(Language).map((language) => (
        <Button
            className="capitalize"
            shape="round"
            key={language}
            onClick={() => setSelectedLanguage(language)}
            type={selectedLanguage.toString() === language ? "primary" : "default"}
        >
            {isMobile
                ? language === Language.Original
                    ? <QuestionOutlined/>
                    : getUnicodeFlagIcon(languageToCountryCode[language])
                : language}
        </Button>
    ));
};

interface LanguageFiltersProps {
    className?: string;
}

const LanguageFilters: React.FC<LanguageFiltersProps> = ({ className = "" }) => {
    return (
        <div className={className + " flex flex-row gap-1 h-full items-center"}>
            <Buttons />
        </div>
    );
};

export default LanguageFilters;

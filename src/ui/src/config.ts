export const getBackendUrl = (): string => {
    const env = import.meta.env.VITE_APP_ENV;
    switch (env) {
        case "dev":
            return "dev-api.ironwatchers.com";
        case "staging":
            return "stage-api.ironwatchers.com";
        case "prod":
            return "api.ironwatchers.com";
        default:
            return "";
    }
};

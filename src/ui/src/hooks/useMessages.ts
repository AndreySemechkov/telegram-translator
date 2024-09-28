import { useContext, useEffect, useState } from "react";
import axios from "axios";

import { getBackendUrl } from "../config";
import { Message } from "../types";
import { MainAppContext } from "../context/MainAppContext";

interface Props {
    limit: number;
    page: number;
}

type FetchState = {
    data?: { messages: Message[]; totalCount: number };
    isLoading: boolean;
    error: boolean;
};

export const useMessages = ({ limit, page }: Props): FetchState => {
    const { query } = useContext(MainAppContext);

    const [fetchState, setFetchState] = useState<FetchState>({ data: undefined, isLoading: false, error: false });

    useEffect(() => {
        setFetchState({ ...fetchState, isLoading: true });

        const fetchData = async () => {
            try {
                const response = await axios.get(`https://${getBackendUrl()}/messages/messages`, {
                    params: { page, limit, query },
                });

                setFetchState({ ...fetchState, isLoading: false, data: response.data });
            } catch (error) {
                setFetchState({ ...fetchState, isLoading: false, error: true });
            }
        };

        fetchData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [limit, page, query]);

    return fetchState;
};

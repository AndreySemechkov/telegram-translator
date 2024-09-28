import { useEffect, useContext } from "react";

import { MainAppContext, MainAppProvider } from "../context/MainAppContext";
import { useMessages } from "../hooks/useMessages";
import Footer from "../components/Footer";
import Header from "../components/Header";
import Loader from "../components/Loader";
import MessageCard from "../components/MessageCard/MessageCard";

const AuxMainPage = () => {
    const { currentPage, pageSize, setTotalPageCount } = useContext(MainAppContext);

    const { data, isLoading } = useMessages({ page: currentPage, limit: pageSize });
    const { messages = [], totalCount = 0 } = data || {};

    useEffect(() => {
        window.scrollTo({ top: 0, behavior: "smooth" }); // Scroll to top of the page when messages change
        setTotalPageCount(totalCount);
    }, [messages, setTotalPageCount, totalCount]);

    const Cards = () => messages.map((message, idx) => <MessageCard message={message} key={`${message.id}-${idx}`} />);
    ``;

    return (
        <div className="flex flex-col w-full h-screen justify-between">
                <Header />
                {/* Body*/}
                <div className="w-full h-full flex flex-col items-center overflow-scroll">
                    {isLoading ? <Loader /> : <Cards />}
                </div>
                {/* End of Body */}
                <Footer />
        </div>
    );
};

const MainPage = () => (
    <MainAppProvider>
        <AuxMainPage />
    </MainAppProvider>
);

export default MainPage;

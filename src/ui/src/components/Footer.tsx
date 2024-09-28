import { Pagination } from "antd";
import React, { useContext } from "react";
import { MainAppContext } from "../context/MainAppContext";

interface FooterProps {
    className?: string;
}

const Footer: React.FC<FooterProps> = () => {
    const { currentPage, pageSize, setCurrentPage, setPageSize, totalPageCount } = useContext(MainAppContext);

    const handlePageChange = (page: number, pageSize?: number) => {
        setCurrentPage(page);
        if (pageSize) {
            setPageSize(pageSize);
        }
        window.scrollTo({ top: 0, behavior: "smooth" }); // Scroll to top of the page
    };

    return (
        <div className="sticky">
            <Pagination
                className="w-full flex justify-center mt-6 mb-6"
                size="small"
                total={totalPageCount}
                pageSize={pageSize}
                current={currentPage}
                onChange={handlePageChange}
            />
        </div>
    );
};
export default Footer;

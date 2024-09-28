export interface PaginationContextProps {
    currentPage: number;
    pageSize: number;
    totalPageCount: number;

    setCurrentPage: (pageNumber: number) => void;
    setPageSize: (pageSize: number) => void;
    setTotalPageCount: (totalPageCount: number) => void;
}

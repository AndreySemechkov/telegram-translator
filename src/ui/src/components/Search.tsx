import { Input } from "antd";
import { useContext, useState } from "react";
import { isMobile } from "react-device-detect";
import { MainAppContext } from "../context/MainAppContext";

const { Search } = Input;

const desktopClassNames = "w-1/2";
const mobileClassNames = "w-5/6";
const className = "self-center " + (isMobile ? mobileClassNames : desktopClassNames);

const SearchInput = () => {
    const { query, setQuery } = useContext(MainAppContext);
    const [value, setValue] = useState(query);

    return (
        <div className={className}>
            <Search
                enterButton="Search"
                onChange={(e) => setValue(e.target.value)}
                onSearch={() => setQuery(value)}
                placeholder="Input search text"
                style={{ borderRadius: "20px"}}
                value={value}
            />
        </div>
    );
};

{
    /** TODO: Implement search logic */
}

export default SearchInput;

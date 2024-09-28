import { Route, Routes } from "react-router-dom";
import MainPage from "./pages/MainPage";
import NoMatchPage from "./pages/NoMatchPage";

const App = () => (
    <div>
        <Routes>
            <Route path="/">
                <Route index element={<MainPage />} />
                <Route path="main" element={<MainPage />} />
                {/* Using path="*" means "match anything", so this route
                acts like a catch-all for URLs that we don't have explicit
                routes for. */}
                <Route path="*" element={<NoMatchPage />} />
            </Route>
        </Routes>
    </div>
);

export default App;

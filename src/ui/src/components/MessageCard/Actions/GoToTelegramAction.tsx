import { Button, Tooltip } from "antd";
import { LinkOutlined } from "@ant-design/icons";

import { ActionProps } from "./types";

const GoToTelegramAction: React.FC<ActionProps> = ({ message }) => {
    const clickHandler = () => {
        window.open(message.link, "_blank");
    };

    return (
        <Tooltip title="Goto Telegram">
            <Button disabled={!message.link} icon={<LinkOutlined />} onClick={clickHandler} type="primary">
                <div className="hidden sm:inline-block">{"Telegram"}</div>
            </Button>
        </Tooltip>
    );
};

export default GoToTelegramAction;

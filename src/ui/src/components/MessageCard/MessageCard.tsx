import _ from "lodash";
import { Card } from "antd";
import { isMobile } from "react-device-detect";
import { useContext } from "react";

import { Language, Message } from "../../types";
import { MainAppContext } from "../../context/MainAppContext";
import GoToTelegramAction from "./Actions/GoToTelegramAction";
import MessageCardMedia from "./MessageCardMedia";
import MessageCardTitle from "./MessageCardTitle";
import ShareAction from "./Actions/ShareAction";

const { Meta } = Card;

interface MessageCardProps {
    message: Message;
}

// Design class names
const desktopClassNames = "mx-auto px-4 w-1/2";
const mobileClassNames = "px-5 w-full";
const className = "pt-4 " + (isMobile ? mobileClassNames : desktopClassNames);

const MessageCard: React.FC<MessageCardProps> = ({ message }) => {
    const { selectedLanguage, showMedia } = useContext(MainAppContext);

    // Card
    const actions = [<GoToTelegramAction message={message} />, <ShareAction message={message} />];
    const CardTitle = <MessageCardTitle message={message} />;

    // Card meta
    const title = _.truncate(message.title, {
        length: isMobile ? 22 : 50,
        omission: "...",
    });

    let description;
    switch (selectedLanguage) {
        case Language.English:
            description = message.english;
            break;
        case Language.Hebrew:
            description = message.hebrew;
            break;
        // Original
        default:
            description = message.message;
    }

    const renderMedia = message.media_url !== "" && showMedia;
    return (
        <div className={className}>
            <Card
                style={{ borderColor:"lightgray", borderRadius:"20px", overflow:"hidden", width:"full" }}
                actions={actions}
                title={CardTitle}
            >
                <div className={"flex " + (isMobile ? "flex-col gap-2" : "flex-row gap-2") + "  w-full"}>
                    <Meta
                        className={`flex-initial ${!isMobile && renderMedia ? "basis-3/4 pr-4" : ""}`}
                        title={title}
                        description={description}
                    />
                    {renderMedia && <MessageCardMedia message={message} />}
                </div>
            </Card>
        </div>
    );
};

export default MessageCard;

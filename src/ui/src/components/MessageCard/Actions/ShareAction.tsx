import _ from "lodash";
import { ActionProps } from "./types";
import {
    EmailIcon,
    EmailShareButton,
    FacebookIcon,
    FacebookShareButton,
    LinkedinIcon,
    LinkedinShareButton,
    RedditIcon,
    RedditShareButton,
    TelegramIcon,
    TelegramShareButton,
    WhatsappIcon,
    WhatsappShareButton,
} from "react-share";
import React from "react";

const shareButtons = [
    { Button: WhatsappShareButton, Icon: WhatsappIcon },
    { Button: TelegramShareButton, Icon: TelegramIcon },
    { Button: FacebookShareButton, Icon: FacebookIcon },
    { Button: LinkedinShareButton, Icon: LinkedinIcon },
    { Button: RedditShareButton, Icon: RedditIcon },
    { Button: EmailShareButton, Icon: EmailIcon },
];

const ShareAction: React.FC<ActionProps> = () => {
    const url = window.location.href;
    return (
        <div>
            {_.map(shareButtons, ({ Button, Icon }) => (
                <Button url={url} key={Button.name}>
                    <Icon size={32} round />
                </Button>
            ))}
        </div>
    );
};

export default ShareAction;

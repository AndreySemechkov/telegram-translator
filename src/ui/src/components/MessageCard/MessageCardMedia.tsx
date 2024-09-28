import { Image } from "antd";

import MessageCardBaseProps from "./MessageCardProps";

const MessageCardMedia: React.FC<MessageCardBaseProps> = ({ message }) => (
    <div className="ml-auto basis-1/4">
        <Image
            src={message.media_url}
        />
    </div>
);

export default MessageCardMedia;

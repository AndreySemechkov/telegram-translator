import MessageCardBaseProps from "./MessageCardProps";

const MessageCardExtra: React.FC<MessageCardBaseProps> = ({ message }) => (
    <div className="flex" style={{ textAlign: "left" }}>
        <div>
            date: {new Date(message.date * 1000).toISOString()}
        </div>
        <div>
            Link: <a href={message.link}>{message.link}</a>
        </div>
    </div>
);

export default MessageCardExtra;

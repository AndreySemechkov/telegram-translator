import MessageCardBaseProps from "./MessageCardProps";

const MessageCardTitle: React.FC<MessageCardBaseProps> = ({ message }) => {
    const date = new Date(message.date * 1000);
    const day = date.toLocaleDateString();
    const time = date.toLocaleTimeString();

    return (
        <div >
            Date: {`${day} ${time}`} Username: {message.username}
        </div>
    );
}

export default MessageCardTitle;

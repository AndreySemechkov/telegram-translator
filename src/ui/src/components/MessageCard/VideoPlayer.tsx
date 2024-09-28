import ReactPlayer from "react-player";

const VideoPlayer = () => (
    <ReactPlayer
        url="https://www.youtube.com/watch?v=vzTrLpxPF54"
        playing={false}
        controls
        width="100%"
        height="200px"
    />
);

export default VideoPlayer;

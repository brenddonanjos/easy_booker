import { Button } from "antd";
import {
  AudioOutlined,
  CloseOutlined,
  LoadingOutlined,
  PauseOutlined,
  SendOutlined,
} from "@ant-design/icons";
import "./style.css";

interface AudioRecorderButtonProps {
  onStartRecording: () => void;
  onStopRecording: () => void;
  onSendAudio: () => void;
  onCancelRecording: () => void;
  audioState: "idle" | "recording" | "recorded" | "sending";
  audioURL: string | null;
  recordingTime: number;
  isAuthenticated: boolean;
}

function AudioRecorderButton(props: AudioRecorderButtonProps) {
  const handleClick = () => {
    if (props.audioState === "recording") {
      props.onStopRecording();
    } else {
      props.onStartRecording();
    }
  };
  const getRecordButtonAttributes = () => {
    switch (props.audioState) {
      case "idle":
        return {
          icon: <AudioOutlined />,
          className: "idle",
          background: "linear-gradient(135deg, #13C2C2, #1890ff)",
          boxShadow:
            "0 0 15px rgba(19, 194, 194, 0.4), 0 0 30px rgba(19, 194, 194, 0.2)",
        };

      case "recording":
        return {
          icon: <PauseOutlined />,
          className: "recording",
          background: "linear-gradient(135deg, #ff4d4f, #ff7a45)",
          boxShadow:
            "0 0 15px rgba(255, 77, 79, 0.4), 0 0 30px rgba(255, 77, 79, 0.2)",
        };
    }
  };

  const getSendButtonAttributes = () => {
    switch (props.audioState) {
      case "recorded":
        return {
          icon: <SendOutlined />,
          className: "recorded",
          background: "linear-gradient(135deg, #52c41a, #73d13d)",
          boxShadow:
            "0 0 15px rgba(82, 196, 26, 0.4), 0 0 30px rgba(82, 196, 26, 0.2)",
        };

      case "sending":
        return {
          icon: <LoadingOutlined spin />,
          className: "sending",
          background: "linear-gradient(135deg, #722ed1, #9254de)",
          boxShadow:
            "0 0 15px rgba(114, 46, 209, 0.4), 0 0 30px rgba(114, 46, 209, 0.2)",
        };
    }
  };

  const recordButtonAttributes = getRecordButtonAttributes();
  const sendButtonAttributes = getSendButtonAttributes();
  return (
    <div className="audio-recorder-container">
      {!props.audioURL && (
        <>
          <Button
            type="primary"
            shape="circle"
            size="large"
            onClick={handleClick}
            icon={recordButtonAttributes?.icon}
            className={`futuristic-record-button desktop-button ${recordButtonAttributes?.className}`}
            disabled={props.audioState === "sending" || !props.isAuthenticated}
            style={{
              background: recordButtonAttributes?.background,
              boxShadow: recordButtonAttributes?.boxShadow,
              opacity: props.audioState === "sending" ? 0.8 : 1,
            }}
          ></Button>
          <div className="sound-waves">
            {[1, 2, 3, 4, 5].map((i) => (
              <div
                key={i}
                className={`wave wave-${i} ${
                  props.audioState === "recording" ? "active" : ""
                }`}
              />
            ))}
          </div>
        </>
      )}
      {props.audioURL && (
        <>
          <div className="recorded-audio-buttons-container">
            <Button
              type="primary"
              shape="circle"
              size="large"
              onClick={props.onCancelRecording}
              icon={<CloseOutlined />}
              className={`futuristic-record-button cancel-button`}
              disabled={
                props.audioState === "sending" || props.audioState === "idle"
              }
            ></Button>

            <Button
              type="primary"
              shape="circle"
              size="large"
              onClick={props.onSendAudio}
              icon={sendButtonAttributes?.icon}
              className={`futuristic-record-button ${sendButtonAttributes?.className}`}
              disabled={props.audioState === "sending"}
              style={{
                background: sendButtonAttributes?.background,
                boxShadow: sendButtonAttributes?.boxShadow,
                opacity: props.audioState === "sending" ? 0.8 : 1,
              }}
            ></Button>
          </div>
        </>
      )}
      <div className={`audio-visualization ${!props.audioURL ? "hidden" : ""}`}>
        <h3>Áudio Gravado:</h3>
        <audio controls src={props.audioURL ?? undefined} />
      </div>
    </div>
  );
}

export default AudioRecorderButton;

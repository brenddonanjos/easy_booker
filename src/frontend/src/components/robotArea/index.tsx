import bot_neutral from "../../assets/neutral_robot.png";
import bot_hearing from "../../assets/hearing_robot.png";
import bot_registering from "../../assets/registering_robot.png";
import bot_waiting from "../../assets/waiting_robot.png";
import bot_success from "../../assets/success_robot.png";
import bot_error from "../../assets/error_robot.png";
import { Card, Typography } from "antd";
import "./style.css";
import type { ResponseSchedule } from "../../interfaces/responseSchedule";

interface RobotAreaProps {
  audioState: "idle" | "recording" | "recorded" | "sending";
  responseSchedule?: ResponseSchedule | null;
}

function RobotArea(props: RobotAreaProps) {
  const getRobotImage = () => {
    if (props.responseSchedule) {
      if (props.responseSchedule.success) {
        return bot_success;
      }
      return bot_error;
    }

    switch (props.audioState) {
      case "idle":
        return bot_neutral;
      case "recording":
        return bot_hearing;
      case "recorded":
        return bot_waiting;
      case "sending":
        return bot_registering;
      default:
        return bot_neutral;
    }
  };

  const getCardTextStyle = () => {
    if (props.responseSchedule) {
      if (props.responseSchedule.success) {
        return "success";
      }
      return "error";
    }
    if (props.audioState === "sending") {
      return "warning";
    }
    return "neutral";
  };

  const getRobotText = () => {
    if (props.responseSchedule && props.responseSchedule.message) {
      let msg = props.responseSchedule.message;
      if (props.responseSchedule.success && props.responseSchedule.link) {
        return (
          <>
            {msg}{" "}
            <a
              href={props.responseSchedule.link}
              target="_blank"
              rel="noopener noreferrer"
              className="schedule-link"
            >
              CLIQUE AQUI
            </a>{" "}
            para acessar o evento
          </>
        );
      }
      if (!props.responseSchedule.success) {
        if (msg.length > 100) msg = msg.substring(0, 100) + "...";

        return <div className="robot-error-message">{msg}</div>;
      }

      return msg;
    }

    switch (props.audioState) {
      case "recording":
        return "Estou ouvindo...";
      case "recorded":
        return "O áudio foi gravado com sucesso, me envie para realizar o agendamento! Ou grave novamente!";
      case "sending":
        return "Estou registrando seu compromisso...";
      default:
        return "Olá! Eu sou o Booker. Me fale sobre seu compromisso, que eu agendo e te dou as melhores dicas";
    }
  };

  const robotImage = getRobotImage();
  const robotText = getRobotText();
  const cardTextStyle = getCardTextStyle();

  return (
    <>
      <div className="robot-section">
        <h2>Easy Booker</h2>
        <img
          src={robotImage}
          alt="RobSom"
          className="robot-image"
          height={140}
        />
        <Card className={`robot-response-card ${cardTextStyle}`} size="small">
          <Typography.Text className="robot-text">{robotText}</Typography.Text>
        </Card>
      </div>
    </>
  );
}

export default RobotArea;

import React from "react";

import { Message } from "../../../types";

export interface ActionProps {
    message: Message
}

export interface GenericButtonProps {
    href?: string;
    icon?: JSX.Element;
    onClick?: React.ReactEventHandler;
    type: string
}

export interface GenericActionProps {
    href?: string;
    IconComponent?: JSX.Element;
    onClick?: React.ReactEventHandler;
    title: string;
    tooltipTitle?: string;
}

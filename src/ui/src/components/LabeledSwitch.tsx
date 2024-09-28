import { Switch, Typography } from "antd";

interface Props {
    checked: boolean;
    className?: string;
    label: string;
    onChange(): void;
}

const LabeledSwitch = ({ checked, className, label, onChange }: Props) => {
    return (
        <div className={className}>
            <Typography.Text className="mr-2">{label}</Typography.Text>
            <Switch checkedChildren="On" unCheckedChildren="Off" checked={checked} onChange={onChange} />
        </div>
    );
};

export default LabeledSwitch;

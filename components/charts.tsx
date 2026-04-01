"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

type ChartDatum = {
  label: string;
  value: number;
};

const colors = ["#c65c2d", "#124c46", "#d5a021", "#5f6fd6", "#7e5032"];

export function SalesBarChart({
  data,
  color = "#c65c2d"
}: {
  data: ChartDatum[];
  color?: string;
}) {
  return (
    <div className="chart-box">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(41, 31, 16, 0.08)" />
          <XAxis dataKey="label" stroke="#6d6459" fontSize={12} />
          <YAxis stroke="#6d6459" fontSize={12} />
          <Tooltip />
          <Bar dataKey="value" radius={[10, 10, 0, 0]} fill={color} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function MultiColorBarChart({ data }: { data: ChartDatum[] }) {
  return (
    <div className="chart-box">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(41, 31, 16, 0.08)" />
          <XAxis dataKey="label" stroke="#6d6459" fontSize={12} />
          <YAxis stroke="#6d6459" fontSize={12} />
          <Tooltip />
          <Bar dataKey="value" radius={[10, 10, 0, 0]}>
            {data.map((entry, index) => (
              <Cell
                key={`${entry.label}-${index}`}
                fill={colors[index % colors.length]}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

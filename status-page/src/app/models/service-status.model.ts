export enum StatusType {
  OPERATIONAL = 'Operational',
  DEGRADED = 'Degraded',
  DOWN = 'Down'
}

export interface ServiceStatus {
  name: string;
  status: StatusType;
  uptime: number;
  uptimeHistory: Array<{
    timestamp: Date;
    status: StatusType;
  }>;
  lastChecked: Date;
} 
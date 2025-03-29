import { Component, computed, input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ServiceStatus, StatusType } from '../../models/service-status.model';

@Component({
  selector: 'app-status',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.css']
})
export class StatusComponent {
  serviceStatus = input.required<ServiceStatus>();
  
  statusClass = computed(() => {
    const status = this.serviceStatus().status;
    return {
      'operational': status === StatusType.OPERATIONAL,
      'degraded': status === StatusType.DEGRADED,
      'down': status === StatusType.DOWN
    };
  });
  
  uptimeBarClass = computed(() => {
    const uptime = this.serviceStatus().uptime;
    if (uptime >= 99) return 'bg-success';
    if (uptime >= 95) return 'bg-warning';
    return 'bg-danger';
  });
} 
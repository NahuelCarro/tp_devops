import { Component, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StatusComponent } from './components/status/status.component';
import { StatusService } from './services/status.service';
import { StatusType } from './models/service-status.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, StatusComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(public statusService: StatusService) {}
  
  overallStatus = computed(() => {
    const status = this.statusService.getOverallStatus();
    if (status === StatusType.OPERATIONAL) {
      return 'Todos los sistemas operativos';
    } else if (status === StatusType.DEGRADED) {
      return 'Algunos servicios experimentan degradación';
    } else {
      return 'Algunos servicios están caídos';
    }
  });
  
  overallStatusClass = computed(() => {
    const status = this.statusService.getOverallStatus();
    if (status === StatusType.OPERATIONAL) {
      return 'alert-success';
    } else if (status === StatusType.DEGRADED) {
      return 'alert-warning';
    } else {
      return 'alert-danger';
    }
  });
} 
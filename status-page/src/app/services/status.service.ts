import { Injectable, signal } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, interval, map, of, tap } from 'rxjs';
import { ServiceStatus, StatusType } from '../models/service-status.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class StatusService {
  // Usar signals para estado reactivo en Angular 18
  //Comentario de prueba
  public serviceStatuses = signal<ServiceStatus[]>([
    {
      name: 'Servicio de Apostador',
      status: StatusType.OPERATIONAL,
      uptime: 100,
      uptimeHistory: Array(90).fill(0).map((_, i) => ({
        timestamp: new Date(Date.now() - (89 - i) * 24 * 60 * 60 * 1000),
        status: StatusType.OPERATIONAL
      })),
      lastChecked: new Date()
    },
    {
      name: 'Servicio de Carrera',
      status: StatusType.OPERATIONAL,
      uptime: 100,
      uptimeHistory: Array(90).fill(0).map((_, i) => ({
        timestamp: new Date(Date.now() - (89 - i) * 24 * 60 * 60 * 1000),
        status: StatusType.OPERATIONAL
      })),
      lastChecked: new Date()
    }
  ]);

  private apiBaseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {
    // Configurar verificación periódica cada 30 segundos
    interval(30000).subscribe(() => {
      console.log('Verificando servicios...');
      this.checkServices();
    });
    
    // Verificar servicios inmediatamente al iniciar
    console.log('Verificación inicial de servicios...');
    setTimeout(() => this.checkServices(), 1000); // Pequeño retraso para asegurar que la app esté lista
  }

  private checkServices(): void {
    this.checkService('apostador');
    this.checkService('listarCarrera');
    this.checkService('crearCarrera');
  }

  private mapHttpError(httpError: number): StatusType {
    switch (httpError) {
      case 0:
        // CORS o sin conexión
        return StatusType.DOWN;
      case 400:
        return StatusType.DEGRADED;
      case 401:
        return StatusType.DOWN;
      default:
        return StatusType.DOWN;
    }
  }

  private getEndpoint(serviceName: string): string {
    var path = null;
    switch (serviceName) {
    case "apostador":
      path = '/apostador/login';
      break;
    case "listarCarrera":
      path = '/carrera/listar';
      break;
    case "crearCarrera":
      path = '/carrera/crear';
      break;
    default:
      console.log("Ha ocurrido un error");
  }

    return environment.useProxy ? `${this.apiBaseUrl}${path}` : `${this.apiBaseUrl}${path}`;
  }

  private checkService(serviceName: string): void {
    const endpoint = this.getEndpoint(serviceName);
    console.log(`Verificando servicio ${serviceName} en ${endpoint}`);
    
    // Configuración de encabezados para las solicitudes
    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json'
    });

    // Añadimos un timeout para evitar esperas largas cuando el servidor no responde
    const options = { 
      headers, 
      observe: 'response' as 'response',  // Observar respuesta completa para ver códigos de estado
      responseType: 'text' as 'json'      // Evitar errores de parsing JSON en respuestas vacías
    };

    if (serviceName === 'apostador') {
      // Para el login, OAuth2 espera datos codificados como form-urlencoded
      const body = 'username=test%40test.com&password=wrong_password';
      
      this.http.post(endpoint, body, options)
        .pipe(
          map(response => {
            console.log(`Servicio de apostador respondió con código: ${response.status}`);
            return StatusType.OPERATIONAL;
          }),
          catchError(error => {
            console.log(`Error en servicio de apostador: ${error.status} - ${error.message}`);
            console.log('Detalles del error:', error);
            
            return of(this.mapHttpError(error.status));
          })
        )
        .subscribe(status => {
          const currentStatuses = this.serviceStatuses();
          const apostadorIndex = currentStatuses.findIndex((s: ServiceStatus) => s.name === 'Servicio de Apostador');
          if (apostadorIndex !== -1) {
            const updatedStatuses = [...currentStatuses];
            // Actualizar historial y uptime
            const newHistory = [
              ...updatedStatuses[apostadorIndex].uptimeHistory.slice(1),
              { timestamp: new Date(), status }
            ];
            const operationalDays = newHistory.filter(h => h.status === StatusType.OPERATIONAL).length;
            updatedStatuses[apostadorIndex] = {
              ...updatedStatuses[apostadorIndex],
              status,
              lastChecked: new Date(),
              uptimeHistory: newHistory,
              uptime: (operationalDays / newHistory.length) * 100
            };
            this.serviceStatuses.set(updatedStatuses);
          }
        });
    } else if(serviceName === 'crearCarrera') {
      const body = 'fecha=2025-01-01';

      this.http.post(endpoint, body, options)
        .pipe(
          map(response => {
            console.log(`Servicio de carrera respondió con código: ${response.status}`);
            return StatusType.OPERATIONAL;
          }),
          catchError(error => {
            console.log(`Error en servicio de carrera: ${error.status} - ${error.message}`);
            console.log('Detalles del error:', error);
            
            return of(this.mapHttpError(error.status));
          })
        )
        .subscribe(status => {
          const currentStatuses = this.serviceStatuses();
          const carreraIndex = currentStatuses.findIndex((s: ServiceStatus) => s.name === 'Servicio de Carrera');
          if (carreraIndex !== -1) {
            const updatedStatuses = [...currentStatuses];
            // Actualizar historial y uptime
            const newHistory = [
              ...updatedStatuses[carreraIndex].uptimeHistory.slice(1),
              { timestamp: new Date(), status }
            ];
            const operationalDays = newHistory.filter(h => h.status === StatusType.OPERATIONAL).length;
            updatedStatuses[carreraIndex] = {
              ...updatedStatuses[carreraIndex],
              status,
              lastChecked: new Date(),
              uptimeHistory: newHistory,
              uptime: (operationalDays / newHistory.length) * 100
            };
            this.serviceStatuses.set(updatedStatuses);
          }
        });
    } else if(serviceName === 'listarCarrera') {
      this.http.get(endpoint, options)
        .pipe(
          map(response => {
            console.log(`Servicio de carrera respondió con código: ${response.status}`);
            return StatusType.OPERATIONAL;
          }),
          catchError(error => {
            console.log(`Error en servicio de carrera: ${error.status} - ${error.message}`);
            console.log('Detalles del error:', error);
            
            return of(this.mapHttpError(error.status));
          })
        )
        .subscribe(status => {
          const currentStatuses = this.serviceStatuses();
          const carreraIndex = currentStatuses.findIndex((s: ServiceStatus) => s.name === 'Servicio de Carrera');
          if (carreraIndex !== -1) {
            const updatedStatuses = [...currentStatuses];
            // Actualizar historial y uptime también para listarCarrera
            const newHistory = [
              ...updatedStatuses[carreraIndex].uptimeHistory.slice(1),
              { timestamp: new Date(), status }
            ];
            const operationalDays = newHistory.filter(h => h.status === StatusType.OPERATIONAL).length;
            updatedStatuses[carreraIndex] = {
              ...updatedStatuses[carreraIndex],
              status,
              lastChecked: new Date(),
              uptimeHistory: newHistory,
              uptime: (operationalDays / newHistory.length) * 100
            };
            this.serviceStatuses.set(updatedStatuses);
          }
        });
    }
  }

  getOverallStatus(): StatusType {
    const services = this.serviceStatuses();
    if (services.some(s => s.status === StatusType.DOWN)) {
      return StatusType.DOWN;
    }
    if (services.some(s => s.status === StatusType.DEGRADED)) {
      return StatusType.DEGRADED;
    }
    return StatusType.OPERATIONAL;
  }
}
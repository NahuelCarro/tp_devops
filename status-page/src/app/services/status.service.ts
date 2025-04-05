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
    this.checkService('carrera');
  }

  private getEndpoint(serviceName: string): string {
    const path = serviceName === 'apostador' ? '/apostador/login' : '/carrera/listar';
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
            
            // Si hay error 401 o 422, está funcionando (error de credenciales esperado)
            if (error.status === 401 || error.status === 422) {
              return of(StatusType.OPERATIONAL);
            } 
            
            // CORS generalmente produce status 0 - lo tratamos como servicio caído
            if (error.status === 0) {
              console.error('Error de conexión al servicio de apostador. Probable problema de CORS.');
              console.error('Solución: Agrega middleware CORS a tu API o configura un proxy en Angular.');
              return of(StatusType.DOWN);
            }
            
            // Otros errores HTTP
            if (error.status >= 400 && error.status < 500) {
              return of(StatusType.DEGRADED);
            }
            
            return of(StatusType.DOWN);
          })
        )
        .subscribe(status => {
          const currentStatuses = this.serviceStatuses();
          const apostadorIndex = currentStatuses.findIndex((s: ServiceStatus) => s.name === 'Servicio de Apostador');
          if (apostadorIndex !== -1) {
            const updatedStatuses = [...currentStatuses];
            updatedStatuses[apostadorIndex] = {
              ...updatedStatuses[apostadorIndex],
              status,
              lastChecked: new Date()
            };
            this.serviceStatuses.set(updatedStatuses);
          }
        });
    } else {
      this.http.get(endpoint, options)
        .pipe(
          map(response => {
            console.log(`Servicio de carrera respondió con código: ${response.status}`);
            return StatusType.OPERATIONAL;
          }),
          catchError(error => {
            console.log(`Error en servicio de carrera: ${error.status} - ${error.message}`);
            console.log('Detalles del error:', error);
            
            // CORS generalmente produce status 0 - lo tratamos como servicio caído
            if (error.status === 0) {
              console.error('Error de conexión al servicio de carrera. Probable problema de CORS.');
              console.error('Solución: Agrega middleware CORS a tu API o configura un proxy en Angular.');
              return of(StatusType.DOWN);
            }
            
            // Otros errores HTTP
            if (error.status >= 400 && error.status < 500) {
              return of(StatusType.DEGRADED);
            }
            
            return of(StatusType.DOWN);
          })
        )
        .subscribe(status => {
          const currentStatuses = this.serviceStatuses();
          const carreraIndex = currentStatuses.findIndex((s: ServiceStatus) => s.name === 'Servicio de Carrera');
          if (carreraIndex !== -1) {
            const updatedStatuses = [...currentStatuses];
            updatedStatuses[carreraIndex] = {
              ...updatedStatuses[carreraIndex],
              status,
              lastChecked: new Date()
            };
            this.serviceStatuses.set(updatedStatuses);
          }
        });
    }
  }

  private updateServiceStatus(serviceName: string, status: StatusType): void {
    const services = this.serviceStatuses();
    const serviceIndex = services.findIndex(s => 
      s.name === (serviceName === 'apostador' ? 'Servicio de Apostador' : 'Servicio de Carrera')
    );
    
    if (serviceIndex !== -1) {
      const updatedService = { ...services[serviceIndex] };
      
      // Actualizar historial
      updatedService.uptimeHistory.push({
        timestamp: new Date(),
        status
      });
      
      if (updatedService.uptimeHistory.length > 90) {
        updatedService.uptimeHistory.shift();
      }
      
      // Calcular porcentaje de uptime
      const operationalCount = updatedService.uptimeHistory.filter(
        h => h.status === StatusType.OPERATIONAL
      ).length;
      
      updatedService.uptime = (operationalCount / updatedService.uptimeHistory.length) * 100;
      updatedService.status = status;
      updatedService.lastChecked = new Date();
      
      // Actualizar el signal con el nuevo estado
      const updatedServices = [...services];
      updatedServices[serviceIndex] = updatedService;
      this.serviceStatuses.set(updatedServices);
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
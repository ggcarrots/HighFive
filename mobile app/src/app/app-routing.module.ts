import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadChildren: './pages/login/login.module#LoginModule'
  },
  {
    path: 'dashboard',
    loadChildren: './pages/dashboard/dashboard.module#DashboardPageModule',
    canLoad: [AuthGuard]
  },
  {
    path: 'initiative-details/:id',
    loadChildren: './pages/initiative-details/initiative-details.module#InitiativeDetailsPageModule'
  },
  { path: 'found-success', loadChildren: './pages/found-success/found-success.module#FoundSuccessPageModule' },  { path: 'new-initiative', loadChildren: './pages/new-initiative/new-initiative.module#NewInitiativePageModule' }




];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}

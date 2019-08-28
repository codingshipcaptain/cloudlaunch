import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { HttpService} from '../http.service';
import { Router } from '@angular/router'; //Add ActivatedRoute for activated routes

@Component({
  selector: 'app-shelter',
  templateUrl: './shelter.component.html',
  styleUrls: ['./shelter.component.css']
})
export class ShelterComponent implements OnInit {
    pets:any;

    constructor(private _httpService: HttpService, private _router: Router){}

    ngOnInit() {
        this._httpService.getThings().subscribe(things => {
            console.log('things in things components: ', things);
            this.pets = things;
        })
    }

    show(pet){
        this._router.navigate(['/pets/'+pet._id])
    }

    edit(pet){
        this._router.navigate(['/pets/'+pet._id+'/edit'])
    }
}

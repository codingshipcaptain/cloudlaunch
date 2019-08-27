import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { HttpService} from '../http.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-new',
  templateUrl: './new.component.html',
  styleUrls: ['./new.component.css']
})
export class NewComponent implements OnInit {
    movie: any;
    review: any;
    terr: any;
    errors: any;
    @Input() show;
    @Input() things;
    @Output() changeShow = new EventEmitter();


    constructor(private _httpService: HttpService, private _router: Router){}

    ngOnInit() {
        this.movie = { title: ""};
        this.review = { name: "", ureview: ""};
    }

    addMovie(){
        console.log("MOVIE: ", this.movie)
        console.log("REVIEW: ", this.review)
        this.movie.rating = parseInt(this.review.rating);
        this.movie.reviews = [this.review];
        let pkg = {one: this.movie, review: this.review};
        console.log("THIS IS THE PACKAGE: ", pkg)
        this._httpService.createOne(pkg).subscribe(data => {
            console.log(data);
            if(data['good']) {
                this.things.push(this.movie);
                this.changeShow.emit(false);
            }
            else {
                this.errors = [];
                this.terr = data['tobj']['errors'];
                console.log("ERROR LIST", this.terr);
                if(this.terr.name != undefined){
                    if(this.terr.name.kind == 'required'){
                        this.errors.push('Name is required.');
                    }
                    if(this.terr.name.kind == 'minlength'){
                        this.errors.push('Name must be 3 or more characters.')
                    }
                }
                if(this.terr.rating != undefined){
                    if(this.terr.rating.kind == 'required'){
                        this.errors.push('Rating is required.');
                    }
                }
                if(this.terr.ureview != undefined){
                    if(this.terr.ureview.kind == 'required'){
                        this.errors.push('Review is required.');
                    }
                    if(this.terr.ureview.kind == 'minlength'){
                        this.errors.push('Review must be 3 or more characters.')
                    }
                }
                if(this.terr.title != undefined){
                    if(this.terr.title.kind == 'required'){
                        this.errors.push('Title is required.');
                    }
                    if(this.terr.title.kind == 'minlength'){
                        this.errors.push('Title must be 3 or more characters.')
                    }
                }
            }
        })
    }

    cancel(){this._router.navigate(['/movies'])}
}

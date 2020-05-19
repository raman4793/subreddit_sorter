import { Component } from '@angular/core';
import { SubredditService } from './services/subreddit.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'frontend';
  subreddits;

  constructor(private subredditService: SubredditService){
    this.subredditService.getSubreddits().subscribe(subreddits => {
      this.subreddits = subreddits
      console.log(this.subreddits);
    });
  }

}

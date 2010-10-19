# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Voting'
        db.create_table('voting_voting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('discussion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='voting', to=orm['discussions.Discussion'])),
            ('votes_per_participant', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('percent_voted', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('decision_story', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='voting', null=True, to=orm['discussions.Story'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('voting', ['Voting'])

        # Adding model 'Ballot'
        db.create_table('voting_ballot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ballot', null=True, to=orm['discussions.Story'])),
            ('voting', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ballot', to=orm['voting.Voting'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('voting', ['Ballot'])


    def backwards(self, orm):
        
        # Deleting model 'Voting'
        db.delete_table('voting_voting')

        # Deleting model 'Ballot'
        db.delete_table('voting_ballot')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'common.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'discussions.discussion': {
            'Meta': {'object_name': 'Discussion'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discussions'", 'to': "orm['auth.Group']"}),
            'h': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_related_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '500', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discussions'", 'to': "orm['discussions.DiscussionType']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'w': ('django.db.models.fields.IntegerField', [], {'default': '150'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'discussions.discussiontype': {
            'Meta': {'object_name': 'DiscussionType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'discussions.opinion': {
            'Meta': {'unique_together': "(('discussion', 'slug'),)", 'object_name': 'Opinion'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'opinions'", 'to': "orm['discussions.Discussion']"}),
            'h': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_related_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '500', 'db_index': 'True'}),
            'speech_act': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'opinions'", 'to': "orm['discussions.SpeechAct']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'w': ('django.db.models.fields.IntegerField', [], {'default': '150'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'discussions.speechact': {
            'Meta': {'object_name': 'SpeechAct'},
            'discussion_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'speech_acts'", 'to': "orm['discussions.DiscussionType']"}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'ordinal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'story_type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'discussions.story': {
            'Meta': {'unique_together': "(('discussion', 'slug'),)", 'object_name': 'Story'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': "orm['discussions.Discussion']"}),
            'h': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_parent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_related_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'parent story'", 'null': 'True', 'blank': 'True', 'to': "orm['discussions.Story']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '500', 'db_index': 'True'}),
            'speech_act': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': "orm['discussions.SpeechAct']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'w': ('django.db.models.fields.IntegerField', [], {'default': '150'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'voting.ballot': {
            'Meta': {'object_name': 'Ballot'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ballot'", 'null': 'True', 'to': "orm['discussions.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'voting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ballot'", 'to': "orm['voting.Voting']"})
        },
        'voting.voting': {
            'Meta': {'object_name': 'Voting'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'decision_story': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voting'", 'null': 'True', 'to': "orm['discussions.Story']"}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'voting'", 'to': "orm['discussions.Discussion']"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent_voted': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'votes_per_participant': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['voting']

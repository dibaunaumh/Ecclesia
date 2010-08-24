# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DiscussionType'
        db.create_table('discussions_discussiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('discussions', ['DiscussionType'])

        # Adding model 'Discussion'
        db.create_table('discussions_discussion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('x', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('w', self.gf('django.db.models.fields.IntegerField')(default=150)),
            ('h', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('last_related_update', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='discussions', to=orm['auth.Group'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='discussions', to=orm['discussions.DiscussionType'])),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('discussions', ['Discussion'])

        # Adding model 'SpeechAct'
        db.create_table('discussions_speechact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('discussion_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='speech_acts', to=orm['discussions.DiscussionType'])),
            ('story_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('ordinal', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('discussions', ['SpeechAct'])

        # Adding model 'Opinion'
        db.create_table('discussions_opinion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('x', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('w', self.gf('django.db.models.fields.IntegerField')(default=150)),
            ('h', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('last_related_update', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('discussion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='opinions', to=orm['discussions.Discussion'])),
            ('speech_act', self.gf('django.db.models.fields.related.ForeignKey')(related_name='opinions', to=orm['discussions.SpeechAct'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('discussions', ['Opinion'])

        # Adding unique constraint on 'Opinion', fields ['discussion', 'slug']
        db.create_unique('discussions_opinion', ['discussion_id', 'slug'])

        # Adding model 'Story'
        db.create_table('discussions_story', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('x', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('w', self.gf('django.db.models.fields.IntegerField')(default=150)),
            ('h', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('last_related_update', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('discussion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stories', to=orm['discussions.Discussion'])),
            ('speech_act', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stories', to=orm['discussions.SpeechAct'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='parent story', null=True, blank=True, to=orm['discussions.Story'])),
            ('is_parent', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('discussions', ['Story'])

        # Adding unique constraint on 'Story', fields ['discussion', 'slug']
        db.create_unique('discussions_story', ['discussion_id', 'slug'])

        # Adding model 'StoryRelation'
        db.create_table('discussions_storyrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('x', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('w', self.gf('django.db.models.fields.IntegerField')(default=150)),
            ('h', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('last_related_update', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('discussion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relations', to=orm['discussions.Discussion'])),
            ('speech_act', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relations', to=orm['discussions.SpeechAct'])),
            ('from_story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_relation', to=orm['discussions.Story'])),
            ('to_story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_relation', to=orm['discussions.Story'])),
        ))
        db.send_create_signal('discussions', ['StoryRelation'])

        # Adding unique constraint on 'StoryRelation', fields ['discussion', 'slug']
        db.create_unique('discussions_storyrelation', ['discussion_id', 'slug'])

        # Adding model 'DiscussionConclusion'
        db.create_table('discussions_discussionconclusion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('discussion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['discussions.Discussion'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['discussions.Story'])),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('discussions', ['DiscussionConclusion'])


    def backwards(self, orm):
        
        # Deleting model 'DiscussionType'
        db.delete_table('discussions_discussiontype')

        # Deleting model 'Discussion'
        db.delete_table('discussions_discussion')

        # Deleting model 'SpeechAct'
        db.delete_table('discussions_speechact')

        # Deleting model 'Opinion'
        db.delete_table('discussions_opinion')

        # Removing unique constraint on 'Opinion', fields ['discussion', 'slug']
        db.delete_unique('discussions_opinion', ['discussion_id', 'slug'])

        # Deleting model 'Story'
        db.delete_table('discussions_story')

        # Removing unique constraint on 'Story', fields ['discussion', 'slug']
        db.delete_unique('discussions_story', ['discussion_id', 'slug'])

        # Deleting model 'StoryRelation'
        db.delete_table('discussions_storyrelation')

        # Removing unique constraint on 'StoryRelation', fields ['discussion', 'slug']
        db.delete_unique('discussions_storyrelation', ['discussion_id', 'slug'])

        # Deleting model 'DiscussionConclusion'
        db.delete_table('discussions_discussionconclusion')


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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discussions'", 'to': "orm['discussions.DiscussionType']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'w': ('django.db.models.fields.IntegerField', [], {'default': '150'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'discussions.discussionconclusion': {
            'Meta': {'object_name': 'DiscussionConclusion'},
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['discussions.Discussion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['discussions.Story']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'discussions.discussiontype': {
            'Meta': {'object_name': 'DiscussionType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'discussions.opinion': {
            'Meta': {'unique_together': "(('discussion', 'slug'),)", 'object_name': 'Opinion'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'opinions'", 'to': "orm['discussions.Discussion']"}),
            'h': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_related_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'speech_act': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'opinions'", 'to': "orm['discussions.SpeechAct']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'w': ('django.db.models.fields.IntegerField', [], {'default': '150'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'discussions.speechact': {
            'Meta': {'object_name': 'SpeechAct'},
            'discussion_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'speech_acts'", 'to': "orm['discussions.DiscussionType']"}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'ordinal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'story_type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'discussions.story': {
            'Meta': {'unique_together': "(('discussion', 'slug'),)", 'object_name': 'Story'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': "orm['discussions.Discussion']"}),
            'h': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_parent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_related_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'parent story'", 'null': 'True', 'blank': 'True', 'to': "orm['discussions.Story']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'speech_act': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': "orm['discussions.SpeechAct']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'w': ('django.db.models.fields.IntegerField', [], {'default': '150'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'discussions.storyrelation': {
            'Meta': {'unique_together': "(('discussion', 'slug'),)", 'object_name': 'StoryRelation'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relations'", 'to': "orm['discussions.Discussion']"}),
            'from_story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_relation'", 'to': "orm['discussions.Story']"}),
            'h': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_related_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'speech_act': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relations'", 'to': "orm['discussions.SpeechAct']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'to_story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_relation'", 'to': "orm['discussions.Story']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'w': ('django.db.models.fields.IntegerField', [], {'default': '150'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['discussions']

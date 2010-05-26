
from south.db import db
from django.db import models
from groups.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('groups_userprofile', (
            ('id', orm['groups.UserProfile:id']),
            ('user', orm['groups.UserProfile:user']),
            ('picture', orm['groups.UserProfile:picture']),
        ))
        db.send_create_signal('groups', ['UserProfile'])
        
        # Adding model 'GroupProfile'
        db.create_table('groups_groupprofile', (
            ('id', orm['groups.GroupProfile:id']),
            ('x', orm['groups.GroupProfile:x']),
            ('y', orm['groups.GroupProfile:y']),
            ('w', orm['groups.GroupProfile:w']),
            ('h', orm['groups.GroupProfile:h']),
            ('last_related_update', orm['groups.GroupProfile:last_related_update']),
            ('group', orm['groups.GroupProfile:group']),
            ('slug', orm['groups.GroupProfile:slug']),
            ('description', orm['groups.GroupProfile:description']),
            ('parent', orm['groups.GroupProfile:parent']),
            ('forked_from', orm['groups.GroupProfile:forked_from']),
            ('location', orm['groups.GroupProfile:location']),
            ('created_by', orm['groups.GroupProfile:created_by']),
            ('created_at', orm['groups.GroupProfile:created_at']),
            ('updated_at', orm['groups.GroupProfile:updated_at']),
        ))
        db.send_create_signal('groups', ['GroupProfile'])
        
        # Adding model 'MissionStatement'
        db.create_table('groups_missionstatement', (
            ('id', orm['groups.MissionStatement:id']),
            ('group_profile', orm['groups.MissionStatement:group_profile']),
            ('mission_statement', orm['groups.MissionStatement:mission_statement']),
            ('created_by', orm['groups.MissionStatement:created_by']),
            ('created_at', orm['groups.MissionStatement:created_at']),
            ('updated_at', orm['groups.MissionStatement:updated_at']),
        ))
        db.send_create_signal('groups', ['MissionStatement'])
        
        # Adding model 'GroupPermission'
        db.create_table('groups_grouppermission', (
            ('id', orm['groups.GroupPermission:id']),
            ('group', orm['groups.GroupPermission:group']),
            ('user', orm['groups.GroupPermission:user']),
            ('permission_type', orm['groups.GroupPermission:permission_type']),
        ))
        db.send_create_signal('groups', ['GroupPermission'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('groups_userprofile')
        
        # Deleting model 'GroupProfile'
        db.delete_table('groups_groupprofile')
        
        # Deleting model 'MissionStatement'
        db.delete_table('groups_missionstatement')
        
        # Deleting model 'GroupPermission'
        db.delete_table('groups_grouppermission')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'groups.grouppermission': {
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'permission'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission_type': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'groups.groupprofile': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'forked_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forks'", 'blank': 'True', 'null': 'True', 'to': "orm['groups.GroupProfile']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.Group']"}),
            'h': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_related_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'blank': 'True', 'null': 'True', 'to': "orm['groups.GroupProfile']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'w': ('django.db.models.fields.IntegerField', [], {'default': '150'}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'groups.missionstatement': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'group_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mission_statements'", 'to': "orm['groups.GroupProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mission_statement': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'groups.userprofile': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }
    
    complete_apps = ['groups']
